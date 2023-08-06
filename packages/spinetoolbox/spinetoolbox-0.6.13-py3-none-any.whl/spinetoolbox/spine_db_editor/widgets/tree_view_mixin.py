######################################################################################################################
# Copyright (C) 2017-2022 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Contains the TreeViewMixin class.

:author: M. Marin (KTH)
:date:   26.11.2018
"""
from PySide2.QtCore import Slot
from .add_items_dialogs import (
    AddObjectClassesDialog,
    AddObjectsDialog,
    AddRelationshipClassesDialog,
    AddRelationshipsDialog,
    AddObjectGroupDialog,
    ManageRelationshipsDialog,
    ManageMembersDialog,
)
from .edit_or_remove_items_dialogs import (
    EditObjectClassesDialog,
    EditObjectsDialog,
    EditRelationshipClassesDialog,
    EditRelationshipsDialog,
    RemoveEntitiesDialog,
)
from ..mvcmodels.tool_feature_model import ToolFeatureModel
from ..mvcmodels.parameter_value_list_model import ParameterValueListModel
from ..mvcmodels.alternative_scenario_model import AlternativeScenarioModel
from ..mvcmodels.entity_tree_models import ObjectTreeModel, RelationshipTreeModel
from ...spine_db_parcel import SpineDBParcel


class TreeViewMixin:
    """Provides object and relationship trees for the Spine db editor."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_tree_model = ObjectTreeModel(self, self.db_mngr)
        self.relationship_tree_model = RelationshipTreeModel(self, self.db_mngr)
        self.tool_feature_model = ToolFeatureModel(self, self.db_mngr)
        self.alternative_scenario_model = AlternativeScenarioModel(self, self.db_mngr)
        self.parameter_value_list_model = ParameterValueListModel(self, self.db_mngr)
        models = (
            self.object_tree_model,
            self.relationship_tree_model,
            self.tool_feature_model,
            self.alternative_scenario_model,
            self.parameter_value_list_model,
        )
        views = (
            self.ui.treeView_object,
            self.ui.treeView_relationship,
            self.ui.treeView_tool_feature,
            self.ui.treeView_alternative_scenario,
            self.ui.treeView_parameter_value_list,
        )
        for view, model in zip(views, models):
            view.setModel(model)
            view.connect_spine_db_editor(self)
            view.header().setResizeContentsPrecision(self.visible_rows)

    def connect_signals(self):
        """Connects signals to slots."""
        super().connect_signals()
        self.ui.treeView_object.tree_selection_changed.connect(self.ui.treeView_relationship.clear_any_selections)
        self.ui.treeView_relationship.tree_selection_changed.connect(self.ui.treeView_object.clear_any_selections)

    def init_models(self):
        """Initializes models."""
        super().init_models()
        for view in (
            self.ui.treeView_object,
            self.ui.treeView_relationship,
            self.ui.treeView_tool_feature,
            self.ui.treeView_alternative_scenario,
            self.ui.treeView_parameter_value_list,
        ):
            view.model().db_maps = self.db_maps
            view.model().build_tree()
            for item in view.model().visit_all():
                index = view.model().index_from_item(item)
                view.expand(index)

    @staticmethod
    def _db_map_items(indexes):
        """Groups items from given tree indexes by db map.

        Returns:
            dict: lists of dictionary items keyed by DiffDatabaseMapping
        """
        d = dict()
        for index in indexes:
            item = index.model().item_from_index(index)
            for db_map in item.db_maps:
                d.setdefault(db_map, []).append(item.db_map_data(db_map))
        return d

    def _db_map_ids(self, indexes):
        return self.db_mngr.db_map_ids(self._db_map_items(indexes))

    def _db_map_class_ids(self, indexes):
        return self.db_mngr.db_map_class_ids(self._db_map_items(indexes))

    def export_selected(self, selected_indexes):
        """Exports data from given indexes in the entity tree."""
        parcel = SpineDBParcel(self.db_mngr)
        obj_cls_inds = set(selected_indexes.get("object_class", {}).keys())
        obj_inds = set(selected_indexes.get("object", {}).keys())
        rel_cls_inds = set(selected_indexes.get("relationship_class", {}).keys())
        rel_inds = set(selected_indexes.get("relationship", {}).keys())
        db_map_obj_cls_ids = self._db_map_ids(obj_cls_inds)
        db_map_obj_ids = self._db_map_ids(obj_inds)
        db_map_rel_cls_ids = self._db_map_ids(rel_cls_inds)
        db_map_rel_ids = self._db_map_ids(rel_inds)
        parcel.full_push_object_class_ids(db_map_obj_cls_ids)
        parcel.full_push_object_ids(db_map_obj_ids)
        parcel.full_push_relationship_class_ids(db_map_rel_cls_ids)
        parcel.full_push_relationship_ids(db_map_rel_ids)
        self.export_data(parcel.data)

    def show_add_object_classes_form(self):
        """Shows dialog to add new object classes."""
        dialog = AddObjectClassesDialog(self, self.db_mngr, *self.db_maps)
        dialog.show()

    def show_add_objects_form(self, parent_item):
        """Shows dialog to add new objects."""
        dialog = AddObjectsDialog(self, parent_item, self.db_mngr, *self.db_maps)
        dialog.show()

    def show_add_object_group_form(self, object_class_item):
        """Shows dialog to add new object group."""
        dialog = AddObjectGroupDialog(self, object_class_item, self.db_mngr, *self.db_maps)
        dialog.show()

    def show_manage_members_form(self, object_item):
        """Shows dialog to manage an object group."""
        dialog = ManageMembersDialog(self, object_item, self.db_mngr, *self.db_maps)
        dialog.show()

    def show_add_relationship_classes_form(self, parent_item):
        """Shows dialog to add new relationship_class."""
        dialog = AddRelationshipClassesDialog(self, parent_item, self.db_mngr, *self.db_maps)
        dialog.show()

    def show_add_relationships_form(self, parent_item):
        """Shows dialog to add new relationships."""
        dialog = AddRelationshipsDialog(self, parent_item, self.db_mngr, *self.db_maps)
        dialog.show()

    def show_manage_relationships_form(self, parent_item):
        dialog = ManageRelationshipsDialog(self, parent_item, self.db_mngr, *self.db_maps)
        dialog.show()

    def edit_entity_tree_items(self, selected_indexes):
        """Starts editing given indexes."""
        obj_cls_items = {ind.internalPointer() for ind in selected_indexes.get("object_class", {})}
        obj_items = {ind.internalPointer() for ind in selected_indexes.get("object", {})}
        rel_cls_items = {ind.internalPointer() for ind in selected_indexes.get("relationship_class", {})}
        rel_items = {ind.internalPointer() for ind in selected_indexes.get("relationship", {})}
        self.show_edit_object_classes_form(obj_cls_items)
        self.show_edit_objects_form(obj_items)
        self.show_edit_relationship_classes_form(rel_cls_items)
        self.show_edit_relationships_form(rel_items)

    def show_edit_object_classes_form(self, items):
        if not items:
            return
        dialog = EditObjectClassesDialog(self, self.db_mngr, items)
        dialog.show()

    def show_edit_objects_form(self, items):
        if not items:
            return
        dialog = EditObjectsDialog(self, self.db_mngr, items)
        dialog.show()

    def show_edit_relationship_classes_form(self, items):
        if not items:
            return
        dialog = EditRelationshipClassesDialog(self, self.db_mngr, items)
        dialog.show()

    def show_edit_relationships_form(self, items):
        if not items:
            return
        items_by_class = {}
        for item in items:
            data = item.db_map_data(item.first_db_map)
            relationship_class_name = data["class_name"]
            object_class_name_list = data["object_class_name_list"]
            class_key = (relationship_class_name, object_class_name_list)
            items_by_class.setdefault(class_key, set()).add(item)
        for class_key, classed_items in items_by_class.items():
            dialog = EditRelationshipsDialog(self, self.db_mngr, classed_items, class_key)
            dialog.show()

    @Slot(dict)
    def remove_entity_tree_items(self, selected_indexes):
        """Shows form to remove items from object treeview."""
        selected = {
            item_type: [ind.model().item_from_index(ind) for ind in indexes]
            for item_type, indexes in selected_indexes.items()
        }
        self.show_remove_entity_tree_items_form(selected)

    def show_remove_entity_tree_items_form(self, selected):
        dialog = RemoveEntitiesDialog(self, self.db_mngr, selected)
        dialog.show()

    def receive_alternatives_added(self, db_map_data):
        super().receive_alternatives_added(db_map_data)
        self.alternative_scenario_model.add_alternatives(db_map_data)

    def receive_scenarios_added(self, db_map_data):
        super().receive_scenarios_added(db_map_data)
        self.alternative_scenario_model.add_scenarios(db_map_data)

    def receive_object_classes_added(self, db_map_data):
        super().receive_object_classes_added(db_map_data)
        self.object_tree_model.add_object_classes(db_map_data)

    def receive_objects_added(self, db_map_data):
        super().receive_objects_added(db_map_data)
        self.object_tree_model.add_objects(db_map_data)

    def receive_relationship_classes_added(self, db_map_data):
        super().receive_relationship_classes_added(db_map_data)
        self.object_tree_model.add_relationship_classes(db_map_data)
        self.relationship_tree_model.add_relationship_classes(db_map_data)

    def receive_relationships_added(self, db_map_data):
        super().receive_relationships_added(db_map_data)
        self.object_tree_model.add_relationships(db_map_data)
        self.relationship_tree_model.add_relationships(db_map_data)

    def receive_entity_groups_added(self, db_map_data):
        super().receive_entity_groups_added(db_map_data)
        self.object_tree_model.add_entity_groups(db_map_data)

    def receive_parameter_value_lists_added(self, db_map_data):
        super().receive_parameter_value_lists_added(db_map_data)
        self.parameter_value_list_model.add_parameter_value_lists(db_map_data)

    def receive_list_values_added(self, db_map_data):
        super().receive_list_values_added(db_map_data)
        self.parameter_value_list_model.add_list_values(db_map_data)

    def receive_features_added(self, db_map_data):
        super().receive_features_added(db_map_data)
        self.tool_feature_model.add_features(db_map_data)

    def receive_tools_added(self, db_map_data):
        super().receive_tools_added(db_map_data)
        self.tool_feature_model.add_tools(db_map_data)

    def receive_tool_features_added(self, db_map_data):
        super().receive_tool_features_added(db_map_data)
        self.tool_feature_model.add_tool_features(db_map_data)

    def receive_tool_feature_methods_added(self, db_map_data):
        super().receive_tool_feature_methods_added(db_map_data)
        self.tool_feature_model.add_tool_feature_methods(db_map_data)

    def receive_alternatives_updated(self, db_map_data):
        super().receive_alternatives_updated(db_map_data)
        self.alternative_scenario_model.update_alternatives(db_map_data)

    def receive_scenarios_updated(self, db_map_data):
        super().receive_scenarios_updated(db_map_data)
        self.alternative_scenario_model.update_scenarios(db_map_data)

    def receive_object_classes_updated(self, db_map_data):
        super().receive_object_classes_updated(db_map_data)
        self.object_tree_model.update_object_classes(db_map_data)

    def receive_objects_updated(self, db_map_data):
        super().receive_objects_updated(db_map_data)
        self.object_tree_model.update_objects(db_map_data)

    def receive_relationship_classes_updated(self, db_map_data):
        super().receive_relationship_classes_updated(db_map_data)
        self.object_tree_model.update_relationship_classes(db_map_data)
        self.relationship_tree_model.update_relationship_classes(db_map_data)

    def receive_relationships_updated(self, db_map_data):
        super().receive_relationships_updated(db_map_data)
        self.object_tree_model.update_relationships(db_map_data)
        self.relationship_tree_model.update_relationships(db_map_data)

    def receive_parameter_value_lists_updated(self, db_map_data):
        super().receive_parameter_value_lists_updated(db_map_data)
        self.parameter_value_list_model.update_parameter_value_lists(db_map_data)

    def receive_list_values_updated(self, db_map_data):
        super().receive_list_values_updated(db_map_data)
        self.parameter_value_list_model.update_list_values(db_map_data)

    def receive_features_updated(self, db_map_data):
        super().receive_features_updated(db_map_data)
        self.tool_feature_model.update_features(db_map_data)

    def receive_tools_updated(self, db_map_data):
        super().receive_tools_updated(db_map_data)
        self.tool_feature_model.update_tools(db_map_data)

    def receive_tool_features_updated(self, db_map_data):
        super().receive_tool_features_updated(db_map_data)
        self.tool_feature_model.update_tool_features(db_map_data)

    def receive_tool_feature_methods_updated(self, db_map_data):
        super().receive_tool_feature_methods_updated(db_map_data)
        self.tool_feature_model.update_tool_feature_methods(db_map_data)

    def receive_alternatives_removed(self, db_map_data):
        super().receive_alternatives_removed(db_map_data)
        self.alternative_scenario_model.remove_alternatives(db_map_data)

    def receive_scenarios_removed(self, db_map_data):
        super().receive_scenarios_removed(db_map_data)
        self.alternative_scenario_model.remove_scenarios(db_map_data)

    def receive_object_classes_removed(self, db_map_data):
        super().receive_object_classes_removed(db_map_data)
        self.object_tree_model.remove_object_classes(db_map_data)

    def receive_objects_removed(self, db_map_data):
        super().receive_objects_removed(db_map_data)
        self.object_tree_model.remove_objects(db_map_data)

    def receive_relationship_classes_removed(self, db_map_data):
        super().receive_relationship_classes_removed(db_map_data)
        self.object_tree_model.remove_relationship_classes(db_map_data)
        self.relationship_tree_model.remove_relationship_classes(db_map_data)

    def receive_relationships_removed(self, db_map_data):
        super().receive_relationships_removed(db_map_data)
        self.object_tree_model.remove_relationships(db_map_data)
        self.relationship_tree_model.remove_relationships(db_map_data)

    def receive_entity_groups_removed(self, db_map_data):
        super().receive_entity_groups_removed(db_map_data)
        self.object_tree_model.remove_entity_groups(db_map_data)

    def receive_parameter_value_lists_removed(self, db_map_data):
        super().receive_parameter_value_lists_removed(db_map_data)
        self.parameter_value_list_model.remove_parameter_value_lists(db_map_data)

    def receive_list_values_removed(self, db_map_data):
        super().receive_list_values_removed(db_map_data)
        self.parameter_value_list_model.remove_list_values(db_map_data)

    def receive_features_removed(self, db_map_data):
        super().receive_features_removed(db_map_data)
        self.tool_feature_model.remove_features(db_map_data)

    def receive_tools_removed(self, db_map_data):
        super().receive_tools_removed(db_map_data)
        self.tool_feature_model.remove_tools(db_map_data)

    def receive_tool_features_removed(self, db_map_data):
        super().receive_tool_features_removed(db_map_data)
        self.tool_feature_model.remove_tool_features(db_map_data)

    def receive_tool_feature_methods_removed(self, db_map_data):
        super().receive_tool_feature_methods_removed(db_map_data)
        self.tool_feature_model.remove_tool_feature_methods(db_map_data)
