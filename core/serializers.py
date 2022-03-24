import os
import xml.etree.ElementTree as ET
from rest_framework import serializers

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BUCKET_DIR = os.path.join(BASE_DIR, "bucket")
file_name = "hive_config.xml"


class HiveConfigSerializer(serializers.Serializer):
    """
    Class for the serialization/deserialization of hive xml config data
    """
    bucket = serializers.CharField(max_length=255)
    access_key = serializers.CharField(max_length=255)
    secret_key = serializers.CharField(max_length=255)
    endpoint = serializers.CharField(max_length=255)
    path_style_access = serializers.BooleanField(default=False)
    description = serializers.CharField(max_length=255, required=False, default="")

    def create(self, validated_data):
        """
        append  the validated data to the existing xml doc
        :param validated_data:
        :return:
        """
        path_style_access = "true" if validated_data["path_style_access"] else "false"
        first_property = f"""
            <property>
                <name>fs.s3a.bucket.{validated_data["bucket"]}.access.key</name>
                <value>{validated_data["access_key"]}</value>
            </property>
            """
        second_property = f"""
            <property>
                <name>fs.s3a.bucket.{validated_data["bucket"]}.secret.key</name>
                <value>{validated_data["secret_key"]}</value>
            </property>
            """
        third_property = f"""
            <property>
                <name>fs.s3a.{validated_data["bucket"]}.endpoint</name>
                <value>{validated_data["endpoint"]}</value>
            </property>
            """
        fourth_property = f"""
            <property>
                <name>fs.s3a.{validated_data["bucket"]}.path.style.access</name>
                <value>{path_style_access}</value>
            </property>
        """

        config_file = os.path.join(BUCKET_DIR, file_name)
        child_elements = [first_property, second_property, third_property, fourth_property]

        tree = ET.parse(config_file)
        root = tree.getroot()
        try:
            for prop in child_elements:
                root.append(ET.fromstring(prop))
        except ET.ParseError:
            print("Check the configuration! something went wrong")
            return False

        tree.write(config_file)

        return validated_data
