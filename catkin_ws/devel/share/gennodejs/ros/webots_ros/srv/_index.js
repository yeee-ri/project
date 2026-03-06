
"use strict";

let node_get_name = require('./node_get_name.js')
let field_set_string = require('./field_set_string.js')
let field_get_rotation = require('./field_get_rotation.js')
let camera_get_info = require('./camera_get_info.js')
let gps_decimal_degrees_to_degrees_minutes_seconds = require('./gps_decimal_degrees_to_degrees_minutes_seconds.js')
let node_disable_pose_tracking = require('./node_disable_pose_tracking.js')
let field_get_float = require('./field_get_float.js')
let node_set_visibility = require('./node_set_visibility.js')
let node_set_joint_position = require('./node_set_joint_position.js')
let node_get_status = require('./node_get_status.js')
let field_get_color = require('./field_get_color.js')
let robot_set_mode = require('./robot_set_mode.js')
let field_get_vec3f = require('./field_get_vec3f.js')
let display_get_info = require('./display_get_info.js')
let automobile_get_dimensions = require('./automobile_get_dimensions.js')
let supervisor_movie_start_recording = require('./supervisor_movie_start_recording.js')
let display_draw_polygon = require('./display_draw_polygon.js')
let node_disable_contact_points_tracking = require('./node_disable_contact_points_tracking.js')
let display_image_paste = require('./display_image_paste.js')
let robot_get_device_list = require('./robot_get_device_list.js')
let node_get_orientation = require('./node_get_orientation.js')
let field_get_node = require('./field_get_node.js')
let lidar_get_layer_point_cloud = require('./lidar_get_layer_point_cloud.js')
let field_get_name = require('./field_get_name.js')
let lidar_get_info = require('./lidar_get_info.js')
let field_set_bool = require('./field_set_bool.js')
let speaker_speak = require('./speaker_speak.js')
let node_get_field = require('./node_get_field.js')
let set_float_array = require('./set_float_array.js')
let field_get_string = require('./field_get_string.js')
let field_disable_sf_tracking = require('./field_disable_sf_tracking.js')
let display_set_font = require('./display_set_font.js')
let node_is_proto = require('./node_is_proto.js')
let node_get_id = require('./node_get_id.js')
let field_get_int32 = require('./field_get_int32.js')
let supervisor_get_from_def = require('./supervisor_get_from_def.js')
let supervisor_virtual_reality_headset_get_position = require('./supervisor_virtual_reality_headset_get_position.js')
let get_float_array = require('./get_float_array.js')
let field_set_int32 = require('./field_set_int32.js')
let field_get_count = require('./field_get_count.js')
let skin_get_bone_position = require('./skin_get_bone_position.js')
let skin_set_bone_orientation = require('./skin_set_bone_orientation.js')
let node_add_force_with_offset = require('./node_add_force_with_offset.js')
let display_draw_line = require('./display_draw_line.js')
let get_string = require('./get_string.js')
let lidar_get_layer_range_image = require('./lidar_get_layer_range_image.js')
let field_get_bool = require('./field_get_bool.js')
let get_float = require('./get_float.js')
let node_get_pose = require('./node_get_pose.js')
let node_enable_contact_points_tracking = require('./node_enable_contact_points_tracking.js')
let display_draw_oval = require('./display_draw_oval.js')
let skin_get_bone_orientation = require('./skin_get_bone_orientation.js')
let node_get_static_balance = require('./node_get_static_balance.js')
let node_get_type = require('./node_get_type.js')
let set_string = require('./set_string.js')
let skin_set_bone_position = require('./skin_set_bone_position.js')
let field_set_rotation = require('./field_set_rotation.js')
let field_set_vec3f = require('./field_set_vec3f.js')
let get_uint64 = require('./get_uint64.js')
let set_float = require('./set_float.js')
let node_get_field_by_index = require('./node_get_field_by_index.js')
let supervisor_get_from_id = require('./supervisor_get_from_id.js')
let display_image_load = require('./display_image_load.js')
let field_set_float = require('./field_set_float.js')
let display_draw_pixel = require('./display_draw_pixel.js')
let get_urdf = require('./get_urdf.js')
let lidar_get_frequency_info = require('./lidar_get_frequency_info.js')
let set_bool = require('./set_bool.js')
let camera_get_focus_info = require('./camera_get_focus_info.js')
let node_remove = require('./node_remove.js')
let supervisor_virtual_reality_headset_get_orientation = require('./supervisor_virtual_reality_headset_get_orientation.js')
let display_image_new = require('./display_image_new.js')
let camera_get_zoom_info = require('./camera_get_zoom_info.js')
let get_int = require('./get_int.js')
let node_add_force_or_torque = require('./node_add_force_or_torque.js')
let speaker_is_sound_playing = require('./speaker_is_sound_playing.js')
let set_int = require('./set_int.js')
let node_reset_functions = require('./node_reset_functions.js')
let supervisor_set_label = require('./supervisor_set_label.js')
let field_remove_node = require('./field_remove_node.js')
let node_get_string = require('./node_get_string.js')
let display_image_copy = require('./display_image_copy.js')
let skin_get_bone_name = require('./skin_get_bone_name.js')
let save_image = require('./save_image.js')
let field_import_node_from_string = require('./field_import_node_from_string.js')
let display_draw_rectangle = require('./display_draw_rectangle.js')
let field_remove = require('./field_remove.js')
let field_set_vec2f = require('./field_set_vec2f.js')
let receiver_get_emitter_direction = require('./receiver_get_emitter_direction.js')
let speaker_play_sound = require('./speaker_play_sound.js')
let node_get_center_of_mass = require('./node_get_center_of_mass.js')
let supervisor_movie_stop_recording = require('./supervisor_movie_stop_recording.js')
let node_get_parent_node = require('./node_get_parent_node.js')
let node_get_number_of_fields = require('./node_get_number_of_fields.js')
let node_set_string = require('./node_set_string.js')
let supervisor_get_from_string = require('./supervisor_get_from_string.js')
let pen_set_ink_color = require('./pen_set_ink_color.js')
let field_enable_sf_tracking = require('./field_enable_sf_tracking.js')
let field_get_type = require('./field_get_type.js')
let node_move_viewpoint = require('./node_move_viewpoint.js')
let display_draw_text = require('./display_draw_text.js')
let robot_wait_for_user_input_event = require('./robot_wait_for_user_input_event.js')
let node_enable_pose_tracking = require('./node_enable_pose_tracking.js')
let mouse_get_state = require('./mouse_get_state.js')
let get_bool = require('./get_bool.js')
let display_image_delete = require('./display_image_delete.js')
let node_get_velocity = require('./node_get_velocity.js')
let field_set_color = require('./field_set_color.js')
let node_get_position = require('./node_get_position.js')
let display_image_save = require('./display_image_save.js')
let field_get_vec2f = require('./field_get_vec2f.js')
let range_finder_get_info = require('./range_finder_get_info.js')
let node_get_contact_points = require('./node_get_contact_points.js')
let node_set_velocity = require('./node_set_velocity.js')
let motor_set_control_pid = require('./motor_set_control_pid.js')

module.exports = {
  node_get_name: node_get_name,
  field_set_string: field_set_string,
  field_get_rotation: field_get_rotation,
  camera_get_info: camera_get_info,
  gps_decimal_degrees_to_degrees_minutes_seconds: gps_decimal_degrees_to_degrees_minutes_seconds,
  node_disable_pose_tracking: node_disable_pose_tracking,
  field_get_float: field_get_float,
  node_set_visibility: node_set_visibility,
  node_set_joint_position: node_set_joint_position,
  node_get_status: node_get_status,
  field_get_color: field_get_color,
  robot_set_mode: robot_set_mode,
  field_get_vec3f: field_get_vec3f,
  display_get_info: display_get_info,
  automobile_get_dimensions: automobile_get_dimensions,
  supervisor_movie_start_recording: supervisor_movie_start_recording,
  display_draw_polygon: display_draw_polygon,
  node_disable_contact_points_tracking: node_disable_contact_points_tracking,
  display_image_paste: display_image_paste,
  robot_get_device_list: robot_get_device_list,
  node_get_orientation: node_get_orientation,
  field_get_node: field_get_node,
  lidar_get_layer_point_cloud: lidar_get_layer_point_cloud,
  field_get_name: field_get_name,
  lidar_get_info: lidar_get_info,
  field_set_bool: field_set_bool,
  speaker_speak: speaker_speak,
  node_get_field: node_get_field,
  set_float_array: set_float_array,
  field_get_string: field_get_string,
  field_disable_sf_tracking: field_disable_sf_tracking,
  display_set_font: display_set_font,
  node_is_proto: node_is_proto,
  node_get_id: node_get_id,
  field_get_int32: field_get_int32,
  supervisor_get_from_def: supervisor_get_from_def,
  supervisor_virtual_reality_headset_get_position: supervisor_virtual_reality_headset_get_position,
  get_float_array: get_float_array,
  field_set_int32: field_set_int32,
  field_get_count: field_get_count,
  skin_get_bone_position: skin_get_bone_position,
  skin_set_bone_orientation: skin_set_bone_orientation,
  node_add_force_with_offset: node_add_force_with_offset,
  display_draw_line: display_draw_line,
  get_string: get_string,
  lidar_get_layer_range_image: lidar_get_layer_range_image,
  field_get_bool: field_get_bool,
  get_float: get_float,
  node_get_pose: node_get_pose,
  node_enable_contact_points_tracking: node_enable_contact_points_tracking,
  display_draw_oval: display_draw_oval,
  skin_get_bone_orientation: skin_get_bone_orientation,
  node_get_static_balance: node_get_static_balance,
  node_get_type: node_get_type,
  set_string: set_string,
  skin_set_bone_position: skin_set_bone_position,
  field_set_rotation: field_set_rotation,
  field_set_vec3f: field_set_vec3f,
  get_uint64: get_uint64,
  set_float: set_float,
  node_get_field_by_index: node_get_field_by_index,
  supervisor_get_from_id: supervisor_get_from_id,
  display_image_load: display_image_load,
  field_set_float: field_set_float,
  display_draw_pixel: display_draw_pixel,
  get_urdf: get_urdf,
  lidar_get_frequency_info: lidar_get_frequency_info,
  set_bool: set_bool,
  camera_get_focus_info: camera_get_focus_info,
  node_remove: node_remove,
  supervisor_virtual_reality_headset_get_orientation: supervisor_virtual_reality_headset_get_orientation,
  display_image_new: display_image_new,
  camera_get_zoom_info: camera_get_zoom_info,
  get_int: get_int,
  node_add_force_or_torque: node_add_force_or_torque,
  speaker_is_sound_playing: speaker_is_sound_playing,
  set_int: set_int,
  node_reset_functions: node_reset_functions,
  supervisor_set_label: supervisor_set_label,
  field_remove_node: field_remove_node,
  node_get_string: node_get_string,
  display_image_copy: display_image_copy,
  skin_get_bone_name: skin_get_bone_name,
  save_image: save_image,
  field_import_node_from_string: field_import_node_from_string,
  display_draw_rectangle: display_draw_rectangle,
  field_remove: field_remove,
  field_set_vec2f: field_set_vec2f,
  receiver_get_emitter_direction: receiver_get_emitter_direction,
  speaker_play_sound: speaker_play_sound,
  node_get_center_of_mass: node_get_center_of_mass,
  supervisor_movie_stop_recording: supervisor_movie_stop_recording,
  node_get_parent_node: node_get_parent_node,
  node_get_number_of_fields: node_get_number_of_fields,
  node_set_string: node_set_string,
  supervisor_get_from_string: supervisor_get_from_string,
  pen_set_ink_color: pen_set_ink_color,
  field_enable_sf_tracking: field_enable_sf_tracking,
  field_get_type: field_get_type,
  node_move_viewpoint: node_move_viewpoint,
  display_draw_text: display_draw_text,
  robot_wait_for_user_input_event: robot_wait_for_user_input_event,
  node_enable_pose_tracking: node_enable_pose_tracking,
  mouse_get_state: mouse_get_state,
  get_bool: get_bool,
  display_image_delete: display_image_delete,
  node_get_velocity: node_get_velocity,
  field_set_color: field_set_color,
  node_get_position: node_get_position,
  display_image_save: display_image_save,
  field_get_vec2f: field_get_vec2f,
  range_finder_get_info: range_finder_get_info,
  node_get_contact_points: node_get_contact_points,
  node_set_velocity: node_set_velocity,
  motor_set_control_pid: motor_set_control_pid,
};
