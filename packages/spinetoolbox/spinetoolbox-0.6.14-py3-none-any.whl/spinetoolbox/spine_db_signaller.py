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
Spine DB Signaller class.

:authors: M. Marin (KTH)
:date:   31.10.2019
"""

from PySide2.QtCore import Slot, QObject
from .helpers import busy_effect


class SpineDBSignaller(QObject):
    """Handles signals from DB manager and channels them to listeners."""

    def __init__(self, db_mngr):
        """Initializes the signaler object.

        Args:
            db_mngr (SpineDBManager)
        """
        super().__init__(db_mngr)
        self.db_mngr = db_mngr
        self.listeners = dict()
        self._deferred_notifications = dict()

    def pause(self, *db_maps):
        """Defers notifications from db_maps until ``resume`` is called."""
        for db_map in db_maps:
            self._deferred_notifications.setdefault(db_map, [])

    def resume(self, *db_maps):
        """Performs deferred notifications."""
        for db_map in db_maps:
            for data, method in self._deferred_notifications.pop(db_map, []):
                method({db_map: data})

    def _defer_notification(self, db_map, data, method):
        """Defer notification if db_map is paused, and returns True. Otherwise returns False."""
        deferred = self._deferred_notifications.get(db_map)
        if deferred is None:
            return False
        deferred.append((data, method))
        return True

    def add_db_map_listener(self, db_map, listener):
        """Adds listener for given db_map."""
        self.listeners.setdefault(listener, set()).add(db_map)

    def remove_db_map_listener(self, db_map, listener):
        """Removes db_map from the maps listener listens to."""
        db_maps = self.listeners.get(listener, set())
        db_maps.discard(db_map)
        if not db_maps:
            # We cannot just pop here because we might be iterating self.listeners
            # in _call_in_listeners().
            self.listeners = {l: db_maps for l, db_maps in self.listeners.items() if l is not listener}

    def db_map_listeners(self, db_map):
        return set(listener for listener, db_maps in self.listeners.items() if db_map in db_maps)

    def db_map_editors(self, db_map):
        """Creates a set of given database map's editors.

        Editors are listeners that are interested whether the database is dirty.
        They are expected to implement ``is_db_map_editor()`` which returns a bool.

        Args:
            db_map (DiffDatabaseMapping): database map

        Returns:
            set: database mapping's editors
        """
        return {
            listener
            for listener in self.db_map_listeners(db_map)
            if getattr(listener, "is_db_map_editor", lambda: False)()
        }

    def connect_signals(self):
        """Connects signals."""
        # Added
        self.db_mngr.scenarios_added.connect(self.receive_scenarios_added)
        self.db_mngr.alternatives_added.connect(self.receive_alternatives_added)
        self.db_mngr.object_classes_added.connect(self.receive_object_classes_added)
        self.db_mngr.objects_added.connect(self.receive_objects_added)
        self.db_mngr.relationship_classes_added.connect(self.receive_relationship_classes_added)
        self.db_mngr.relationships_added.connect(self.receive_relationships_added)
        self.db_mngr.entity_groups_added.connect(self.receive_entity_groups_added)
        self.db_mngr.parameter_definitions_added.connect(self.receive_parameter_definitions_added)
        self.db_mngr.parameter_values_added.connect(self.receive_parameter_values_added)
        self.db_mngr.parameter_value_lists_added.connect(self.receive_parameter_value_lists_added)
        self.db_mngr.list_values_added.connect(self.receive_list_values_added)
        self.db_mngr.features_added.connect(self.receive_features_added)
        self.db_mngr.tools_added.connect(self.receive_tools_added)
        self.db_mngr.tool_features_added.connect(self.receive_tool_features_added)
        self.db_mngr.tool_feature_methods_added.connect(self.receive_tool_feature_methods_added)
        self.db_mngr.metadata_added.connect(self.receive_metadata_added)
        self.db_mngr.entity_metadata_added.connect(self.receive_entity_metadata_added)
        self.db_mngr.parameter_value_metadata_added.connect(self.receive_parameter_value_metadata_added)
        # Updated
        self.db_mngr.scenarios_updated.connect(self.receive_scenarios_updated)
        self.db_mngr.alternatives_updated.connect(self.receive_alternatives_updated)
        self.db_mngr.object_classes_updated.connect(self.receive_object_classes_updated)
        self.db_mngr.objects_updated.connect(self.receive_objects_updated)
        self.db_mngr.relationship_classes_updated.connect(self.receive_relationship_classes_updated)
        self.db_mngr.relationships_updated.connect(self.receive_relationships_updated)
        self.db_mngr.parameter_definitions_updated.connect(self.receive_parameter_definitions_updated)
        self.db_mngr.parameter_values_updated.connect(self.receive_parameter_values_updated)
        self.db_mngr.parameter_value_lists_updated.connect(self.receive_parameter_value_lists_updated)
        self.db_mngr.list_values_updated.connect(self.receive_list_values_updated)
        self.db_mngr.features_updated.connect(self.receive_features_updated)
        self.db_mngr.tools_updated.connect(self.receive_tools_updated)
        self.db_mngr.tool_features_updated.connect(self.receive_tool_features_updated)
        self.db_mngr.tool_feature_methods_updated.connect(self.receive_tool_feature_methods_updated)
        self.db_mngr.metadata_updated.connect(self.receive_metadata_updated)
        self.db_mngr.entity_metadata_updated.connect(self.receive_entity_metadata_updated)
        self.db_mngr.parameter_value_metadata_updated.connect(self.receive_parameter_value_metadata_updated)
        # Removed
        self.db_mngr.scenarios_removed.connect(self.receive_scenarios_removed)
        self.db_mngr.alternatives_removed.connect(self.receive_alternatives_removed)
        self.db_mngr.object_classes_removed.connect(self.receive_object_classes_removed)
        self.db_mngr.objects_removed.connect(self.receive_objects_removed)
        self.db_mngr.relationship_classes_removed.connect(self.receive_relationship_classes_removed)
        self.db_mngr.relationships_removed.connect(self.receive_relationships_removed)
        self.db_mngr.entity_groups_removed.connect(self.receive_entity_groups_removed)
        self.db_mngr.parameter_definitions_removed.connect(self.receive_parameter_definitions_removed)
        self.db_mngr.parameter_values_removed.connect(self.receive_parameter_values_removed)
        self.db_mngr.parameter_value_lists_removed.connect(self.receive_parameter_value_lists_removed)
        self.db_mngr.list_values_removed.connect(self.receive_list_values_removed)
        self.db_mngr.features_removed.connect(self.receive_features_removed)
        self.db_mngr.tools_removed.connect(self.receive_tools_removed)
        self.db_mngr.tool_features_removed.connect(self.receive_tool_features_removed)
        self.db_mngr.tool_feature_methods_removed.connect(self.receive_tool_feature_methods_removed)
        self.db_mngr.metadata_removed.connect(self.receive_metadata_removed)
        self.db_mngr.entity_metadata_removed.connect(self.receive_entity_metadata_removed)
        self.db_mngr.parameter_value_metadata_removed.connect(self.receive_parameter_value_metadata_removed)
        # Commit, rollback, refresh
        self.db_mngr.session_refreshed.connect(self.receive_session_refreshed)
        self.db_mngr.session_committed.connect(self.receive_session_committed)
        self.db_mngr.session_rolled_back.connect(self.receive_session_rolled_back)
        self.db_mngr.error_msg.connect(self.receive_error_msg)

    @Slot(object)
    def receive_scenarios_added(self, db_map_data):
        self._call_in_listeners("receive_scenarios_added", db_map_data)

    @Slot(object)
    def receive_alternatives_added(self, db_map_data):
        self._call_in_listeners("receive_alternatives_added", db_map_data)

    @Slot(object)
    def receive_object_classes_added(self, db_map_data):
        self._call_in_listeners("receive_object_classes_added", db_map_data)

    @Slot(object)
    def receive_objects_added(self, db_map_data):
        self._call_in_listeners("receive_objects_added", db_map_data)

    @Slot(object)
    def receive_relationship_classes_added(self, db_map_data):
        self._call_in_listeners("receive_relationship_classes_added", db_map_data)

    @Slot(object)
    def receive_relationships_added(self, db_map_data):
        self._call_in_listeners("receive_relationships_added", db_map_data)

    @Slot(object)
    def receive_entity_groups_added(self, db_map_data):
        self._call_in_listeners("receive_entity_groups_added", db_map_data)

    @Slot(object)
    def receive_parameter_definitions_added(self, db_map_data):
        self._call_in_listeners("receive_parameter_definitions_added", db_map_data)

    @Slot(object)
    def receive_parameter_values_added(self, db_map_data):
        self._call_in_listeners("receive_parameter_values_added", db_map_data)

    @Slot(object)
    def receive_parameter_value_lists_added(self, db_map_data):
        self._call_in_listeners("receive_parameter_value_lists_added", db_map_data)

    @Slot(object)
    def receive_list_values_added(self, db_map_data):
        self._call_in_listeners("receive_list_values_added", db_map_data)

    @Slot(object)
    def receive_features_added(self, db_map_data):
        self._call_in_listeners("receive_features_added", db_map_data)

    @Slot(object)
    def receive_tools_added(self, db_map_data):
        self._call_in_listeners("receive_tools_added", db_map_data)

    @Slot(object)
    def receive_tool_features_added(self, db_map_data):
        self._call_in_listeners("receive_tool_features_added", db_map_data)

    @Slot(object)
    def receive_tool_feature_methods_added(self, db_map_data):
        self._call_in_listeners("receive_tool_feature_methods_added", db_map_data)

    @Slot(object)
    def receive_metadata_added(self, db_map_data):
        self._call_in_listeners("receive_metadata_added", db_map_data)

    @Slot(object)
    def receive_entity_metadata_added(self, db_map_data):
        self._call_in_listeners("receive_entity_metadata_added", db_map_data)

    @Slot(object)
    def receive_parameter_value_metadata_added(self, db_map_data):
        self._call_in_listeners("receive_parameter_value_metadata_added", db_map_data)

    @Slot(object)
    def receive_scenarios_updated(self, db_map_data):
        self._call_in_listeners("receive_scenarios_updated", db_map_data)

    @Slot(object)
    def receive_alternatives_updated(self, db_map_data):
        self._call_in_listeners("receive_alternatives_updated", db_map_data)

    @Slot(object)
    def receive_object_classes_updated(self, db_map_data):
        self._call_in_listeners("receive_object_classes_updated", db_map_data)

    @Slot(object)
    def receive_objects_updated(self, db_map_data):
        self._call_in_listeners("receive_objects_updated", db_map_data)

    @Slot(object)
    def receive_relationship_classes_updated(self, db_map_data):
        self._call_in_listeners("receive_relationship_classes_updated", db_map_data)

    @Slot(object)
    def receive_relationships_updated(self, db_map_data):
        self._call_in_listeners("receive_relationships_updated", db_map_data)

    @Slot(object)
    def receive_parameter_definitions_updated(self, db_map_data):
        self._call_in_listeners("receive_parameter_definitions_updated", db_map_data)

    @Slot(object)
    def receive_parameter_values_updated(self, db_map_data):
        self._call_in_listeners("receive_parameter_values_updated", db_map_data)

    @Slot(object)
    def receive_parameter_value_lists_updated(self, db_map_data):
        self._call_in_listeners("receive_parameter_value_lists_updated", db_map_data)

    @Slot(object)
    def receive_list_values_updated(self, db_map_data):
        self._call_in_listeners("receive_list_values_updated", db_map_data)

    @Slot(object)
    def receive_features_updated(self, db_map_data):
        self._call_in_listeners("receive_features_updated", db_map_data)

    @Slot(object)
    def receive_tools_updated(self, db_map_data):
        self._call_in_listeners("receive_tools_updated", db_map_data)

    @Slot(object)
    def receive_tool_features_updated(self, db_map_data):
        self._call_in_listeners("receive_tool_features_updated", db_map_data)

    @Slot(object)
    def receive_tool_feature_methods_updated(self, db_map_data):
        self._call_in_listeners("receive_tool_feature_methods_updated", db_map_data)

    @Slot(object)
    def receive_metadata_updated(self, db_map_data):
        self._call_in_listeners("receive_metadata_updated", db_map_data)

    @Slot(object)
    def receive_entity_metadata_updated(self, db_map_data):
        self._call_in_listeners("receive_entity_metadata_updated", db_map_data)

    @Slot(object)
    def receive_parameter_value_metadata_updated(self, db_map_data):
        self._call_in_listeners("receive_parameter_value_metadata_updated", db_map_data)

    @Slot(object)
    def receive_scenarios_removed(self, db_map_data):
        self._call_in_listeners("receive_scenarios_removed", db_map_data)

    @Slot(object)
    def receive_alternatives_removed(self, db_map_data):
        self._call_in_listeners("receive_alternatives_removed", db_map_data)

    @Slot(object)
    def receive_object_classes_removed(self, db_map_data):
        self._call_in_listeners("receive_object_classes_removed", db_map_data)

    @Slot(object)
    def receive_objects_removed(self, db_map_data):
        self._call_in_listeners("receive_objects_removed", db_map_data)

    @Slot(object)
    def receive_relationship_classes_removed(self, db_map_data):
        self._call_in_listeners("receive_relationship_classes_removed", db_map_data)

    @Slot(object)
    def receive_relationships_removed(self, db_map_data):
        self._call_in_listeners("receive_relationships_removed", db_map_data)

    @Slot(object)
    def receive_entity_groups_removed(self, db_map_data):
        self._call_in_listeners("receive_entity_groups_removed", db_map_data)

    @Slot(object)
    def receive_parameter_definitions_removed(self, db_map_data):
        self._call_in_listeners("receive_parameter_definitions_removed", db_map_data)

    @Slot(object)
    def receive_parameter_values_removed(self, db_map_data):
        self._call_in_listeners("receive_parameter_values_removed", db_map_data)

    @Slot(object)
    def receive_parameter_value_lists_removed(self, db_map_data):
        self._call_in_listeners("receive_parameter_value_lists_removed", db_map_data)

    @Slot(object)
    def receive_list_values_removed(self, db_map_data):
        self._call_in_listeners("receive_list_values_removed", db_map_data)

    @Slot(object)
    def receive_features_removed(self, db_map_data):
        self._call_in_listeners("receive_features_removed", db_map_data)

    @Slot(object)
    def receive_tools_removed(self, db_map_data):
        self._call_in_listeners("receive_tools_removed", db_map_data)

    @Slot(object)
    def receive_tool_features_removed(self, db_map_data):
        self._call_in_listeners("receive_tool_features_removed", db_map_data)

    @Slot(object)
    def receive_tool_feature_methods_removed(self, db_map_data):
        self._call_in_listeners("receive_tool_feature_methods_removed", db_map_data)

    @Slot(object)
    def receive_metadata_removed(self, db_map_data):
        self._call_in_listeners("receive_metadata_removed", db_map_data)

    @Slot(object)
    def receive_entity_metadata_removed(self, db_map_data):
        self._call_in_listeners("receive_entity_metadata_removed", db_map_data)

    @Slot(object)
    def receive_parameter_value_metadata_removed(self, db_map_data):
        self._call_in_listeners("receive_parameter_value_metadata_removed", db_map_data)

    @Slot(object)
    def receive_error_msg(self, db_map_error_log):
        self._call_in_listeners("receive_error_msg", db_map_error_log)

    @staticmethod
    def _shared_db_map_data(db_map_data, db_maps):
        return {db_map: data for db_map, data in db_map_data.items() if db_map in db_maps}

    @busy_effect
    def _call_in_listeners(self, callback, db_map_data):
        for listener, db_maps in self.listeners.items():
            shared_db_map_data = self._shared_db_map_data(db_map_data, db_maps)
            if shared_db_map_data:
                try:
                    method = getattr(listener, callback)
                except AttributeError:
                    continue
                for db_map, data in shared_db_map_data.items():
                    if self._defer_notification(db_map, data, method):
                        continue
                    method({db_map: data})

    @Slot(set)
    def receive_session_refreshed(self, db_maps):
        for listener, listener_db_maps in self.listeners.items():
            shared_db_maps = listener_db_maps.intersection(db_maps)
            if shared_db_maps:
                try:
                    listener.receive_session_refreshed(shared_db_maps)
                except AttributeError:
                    pass

    @Slot(set, object)
    def receive_session_committed(self, db_maps, cookie):
        for listener, listener_db_maps in self.listeners.items():
            shared_db_maps = listener_db_maps.intersection(db_maps)
            if shared_db_maps:
                try:
                    listener.receive_session_committed(shared_db_maps, cookie)
                except AttributeError:
                    pass

    @Slot(set)
    def receive_session_rolled_back(self, db_maps):
        for listener, listener_db_maps in self.listeners.items():
            shared_db_maps = listener_db_maps.intersection(db_maps)
            if shared_db_maps:
                try:
                    listener.receive_session_rolled_back(shared_db_maps)
                except AttributeError:
                    pass
