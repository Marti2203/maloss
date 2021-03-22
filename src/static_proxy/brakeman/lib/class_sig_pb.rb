# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: class_sig.proto

require 'google/protobuf'

require 'ast_pb'
Google::Protobuf::DescriptorPool.generated_pool.build do
  add_message "proto.Centroid" do
    optional :x, :double, 1
    optional :y, :double, 2
    optional :z, :double, 3
    optional :w, :int32, 4
  end
  add_message "proto.BasicBlockProto" do
    optional :sequence_number, :int32, 1
    optional :in_degree, :int32, 2
    optional :out_degree, :int32, 3
    optional :in_degree_unexceptional, :int32, 4
    optional :out_degree_unexceptional, :int32, 5
    optional :loop_depth, :int32, 6
    optional :stmt_count, :int32, 7
    repeated :invoked_method_signatures, :string, 8
    repeated :predecessors, :int32, 9
    repeated :successors, :int32, 10
    optional :dominator_sequence_number, :int32, 11
  end
  add_message "proto.MethodAttributeProto" do
    optional :class_name, :string, 1
    optional :method_name, :string, 2
    optional :method_signature, :string, 3
    optional :method_subsignature, :string, 4
    repeated :paramter_types, :string, 5
    optional :return_type, :string, 6
    repeated :local_types, :string, 7
    repeated :string_constants, :string, 8
    repeated :invoked_method_signatures, :string, 9
    repeated :resource_refs, :string, 10
    repeated :statements, :string, 11
    optional :modifiers, :string, 12
    optional :centroid, :message, 13, "proto.Centroid"
    optional :centroid_with_invoke, :message, 14, "proto.Centroid"
    repeated :blocks, :message, 15, "proto.BasicBlockProto"
  end
  add_message "proto.ClassAttributeProto" do
    optional :class_name, :string, 1
    optional :super_class_name, :string, 2
    repeated :interface_class_names, :string, 3
    optional :package_name, :string, 4
    optional :is_entry_point, :bool, 5
    repeated :static_field_strings, :string, 6
    repeated :instance_field_strings, :string, 7
    repeated :permission_strings, :string, 8
    repeated :methods, :message, 9, "proto.MethodAttributeProto"
    optional :outer_class_name, :string, 10
    optional :modifiers, :string, 11
  end
  add_message "proto.ClassRelationProto" do
    optional :classname1, :string, 1
    optional :classname2, :string, 2
    repeated :relation_counters, :message, 3, "proto.ClassRelationProto.RelationCounter"
    optional :classname2_is_application_class, :bool, 4
    repeated :classname2_permissions, :string, 5
  end
  add_message "proto.ClassRelationProto.RelationCounter" do
    optional :relation_type, :enum, 1, "proto.ClassRelationProto.RelationType"
    optional :relation_count, :int32, 2
  end
  add_enum "proto.ClassRelationProto.RelationType" do
    value :INHERITANCE, 0
    value :STATIC_ARRAY_FIELD, 1
    value :STATIC__FIELD, 2
    value :INSTANCE_ARRAY_FIELD, 3
    value :INSTANCE_FIELD, 4
    value :METHOD_ARRAY_PARAMERTER, 5
    value :METHOD_PARAMETER, 6
    value :METHOD_ARRAY_RETURN, 7
    value :METHOD_RETURN, 8
    value :METHOD_ARRAY_LOCAL, 9
    value :METHOD_LOCAL, 10
    value :STMT_ARRAY_REF, 11
    value :STMT_INSTANCE_FIELD_REF, 12
    value :STMT_STATIC_FIELD_REF, 13
    value :STMT_LOCAL_REF, 14
    value :CAST_EXPR, 15
    value :INSTANCE_OF_EXPR, 16
    value :NEW_EXPR, 17
    value :NEW_ARRAY_EXPR, 18
    value :NEW_MULTI_ARRAY_EXPR, 19
    value :INVOKE_EXPR, 20
    value :ICC, 21
    value :IMPL, 22
    value :OUTER_CLASS, 23
    value :ClassRelationNone, 24
  end
  add_message "proto.MethodRelationProto" do
    optional :methodname1, :string, 1
    optional :methodname2, :string, 2
  end
  add_message "proto.ClassMethodRelationProto" do
    optional :classname1, :string, 1
    optional :methodname2, :string, 2
  end
  add_message "proto.MethodClassRelationProto" do
    optional :methodname1, :string, 1
    optional :classname2, :string, 2
  end
  add_message "proto.PkgClassMethodResult" do
    optional :pkg_name, :string, 1
    optional :pkg_version, :string, 2
    optional :language, :enum, 3, "proto.Language"
    optional :input_path, :string, 4
    repeated :classes, :message, 5, "proto.ClassAttributeProto"
    repeated :methods, :message, 6, "proto.MethodAttributeProto"
    repeated :class_pairs, :message, 7, "proto.ClassRelationProto"
    repeated :method_pairs, :message, 8, "proto.MethodRelationProto"
    repeated :class_method_pairs, :message, 9, "proto.ClassMethodRelationProto"
    repeated :method_class_pairs, :message, 10, "proto.MethodClassRelationProto"
    optional :timestamp, :uint64, 11
  end
  add_message "proto.PkgClassMethodResults" do
    repeated :pkgs, :message, 1, "proto.PkgClassMethodResult"
    optional :timestamp, :uint64, 2
  end
end

module Proto
  Centroid = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.Centroid").msgclass
  BasicBlockProto = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.BasicBlockProto").msgclass
  MethodAttributeProto = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.MethodAttributeProto").msgclass
  ClassAttributeProto = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.ClassAttributeProto").msgclass
  ClassRelationProto = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.ClassRelationProto").msgclass
  ClassRelationProto::RelationCounter = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.ClassRelationProto.RelationCounter").msgclass
  ClassRelationProto::RelationType = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.ClassRelationProto.RelationType").enummodule
  MethodRelationProto = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.MethodRelationProto").msgclass
  ClassMethodRelationProto = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.ClassMethodRelationProto").msgclass
  MethodClassRelationProto = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.MethodClassRelationProto").msgclass
  PkgClassMethodResult = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.PkgClassMethodResult").msgclass
  PkgClassMethodResults = Google::Protobuf::DescriptorPool.generated_pool.lookup("proto.PkgClassMethodResults").msgclass
end
