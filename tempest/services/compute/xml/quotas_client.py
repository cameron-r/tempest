# Copyright 2012 NTT Data
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from lxml import etree

from tempest.common import rest_client
from tempest.common import xml_utils
from tempest import config

CONF = config.CONF


def format_quota(q):
    quota = {}
    for k, v in q.items():
        try:
            v = int(v)
        except ValueError:
            pass

        quota[k] = v

    return quota


class QuotasClientXML(rest_client.RestClient):
    TYPE = "xml"

    def __init__(self, auth_provider):
        super(QuotasClientXML, self).__init__(auth_provider)
        self.service = CONF.compute.catalog_type

    def get_quota_set(self, tenant_id, user_id=None):
        """List the quota set for a tenant."""

        url = 'os-quota-sets/%s' % str(tenant_id)
        if user_id:
            url += '?user_id=%s' % str(user_id)
        resp, body = self.get(url)
        body = xml_utils.xml_to_json(etree.fromstring(body))
        body = format_quota(body)
        return resp, body

    def get_default_quota_set(self, tenant_id):
        """List the default quota set for a tenant."""

        url = 'os-quota-sets/%s/defaults' % str(tenant_id)
        resp, body = self.get(url)
        body = xml_utils.xml_to_json(etree.fromstring(body))
        body = format_quota(body)
        return resp, body

    def update_quota_set(self, tenant_id, user_id=None,
                         force=None, injected_file_content_bytes=None,
                         metadata_items=None, ram=None, floating_ips=None,
                         fixed_ips=None, key_pairs=None, instances=None,
                         security_group_rules=None, injected_files=None,
                         cores=None, injected_file_path_bytes=None,
                         security_groups=None):
        """
        Updates the tenant's quota limits for one or more resources
        """
        post_body = xml_utils.Element("quota_set",
                                      xmlns=xml_utils.XMLNS_11)

        if force is not None:
            post_body.add_attr('force', force)

        if injected_file_content_bytes is not None:
            post_body.add_attr('injected_file_content_bytes',
                               injected_file_content_bytes)

        if metadata_items is not None:
            post_body.add_attr('metadata_items', metadata_items)

        if ram is not None:
            post_body.add_attr('ram', ram)

        if floating_ips is not None:
            post_body.add_attr('floating_ips', floating_ips)

        if fixed_ips is not None:
            post_body.add_attr('fixed_ips', fixed_ips)

        if key_pairs is not None:
            post_body.add_attr('key_pairs', key_pairs)

        if instances is not None:
            post_body.add_attr('instances', instances)

        if security_group_rules is not None:
            post_body.add_attr('security_group_rules', security_group_rules)

        if injected_files is not None:
            post_body.add_attr('injected_files', injected_files)

        if cores is not None:
            post_body.add_attr('cores', cores)

        if injected_file_path_bytes is not None:
            post_body.add_attr('injected_file_path_bytes',
                               injected_file_path_bytes)

        if security_groups is not None:
            post_body.add_attr('security_groups', security_groups)

        if user_id:
            resp, body = self.put('os-quota-sets/%s?user_id=%s' %
                                  (str(tenant_id), str(user_id)),
                                  str(xml_utils.Document(post_body)))
        else:
            resp, body = self.put('os-quota-sets/%s' % str(tenant_id),
                                  str(xml_utils.Document(post_body)))

        body = xml_utils.xml_to_json(etree.fromstring(body))
        body = format_quota(body)
        return resp, body

    def delete_quota_set(self, tenant_id):
        """Delete the tenant's quota set."""
        return self.delete('os-quota-sets/%s' % str(tenant_id))


class QuotaClassesClientXML(rest_client.RestClient):
    TYPE = "xml"

    def __init__(self, auth_provider):
        super(QuotaClassesClientXML, self).__init__(auth_provider)
        self.service = CONF.compute.catalog_type

    def get_quota_class_set(self, quota_class_id):
        """List the quota class set for a quota class."""

        url = 'os-quota-class-sets/%s' % str(quota_class_id)
        resp, body = self.get(url)
        body = xml_utils.xml_to_json(etree.fromstring(body))
        body = format_quota(body)
        return resp, body

    def update_quota_class_set(self, quota_class_id, **kwargs):
        """
        Updates the quota class's limits for one or more resources.
        """
        post_body = xml_utils.Element("quota_class_set",
                                      xmlns=xml_utils.XMLNS_11,
                                      **kwargs)

        resp, body = self.put('os-quota-class-sets/%s' % str(quota_class_id),
                              str(xml_utils.Document(post_body)))

        body = xml_utils.xml_to_json(etree.fromstring(body))
        body = format_quota(body)
        return resp, body
