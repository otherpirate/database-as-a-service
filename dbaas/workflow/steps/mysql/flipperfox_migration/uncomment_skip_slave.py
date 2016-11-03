# -*- coding: utf-8 -*-
import logging
from util import full_stack
from util import exec_remote_command
from util import build_context_script
from dbaas_cloudstack.models import HostAttr as CS_HostAttr
from workflow.steps.util.base import BaseStep
from workflow.exceptions.error_codes import DBAAS_0020
from workflow.steps.util import test_bash_script_error
from workflow.steps.mysql.util import build_uncomment_skip_slave_script

LOG = logging.getLogger(__name__)


class UncommentSkipSlave(BaseStep):

    def __unicode__(self):
        return "Uncomment skip_slave_start parameter..."

    def do(self, workflow_dict):
        try:

            for host in workflow_dict['target_hosts']:
                cs_host_attr = CS_HostAttr.objects.get(host=host)

                script = test_bash_script_error()
                script += build_uncomment_skip_slave_script()

                script = build_context_script({}, script)

                output = {}
                LOG.info(script)
                return_code = exec_remote_command(server=host.address,
                                                  username=cs_host_attr.vm_user,
                                                  password=cs_host_attr.vm_password,
                                                  command=script,
                                                  output=output)
                LOG.info(output)
                if return_code != 0:
                    raise Exception(str(output))

            return True
        except Exception:
            traceback = full_stack()

            workflow_dict['exceptions']['error_codes'].append(DBAAS_0020)
            workflow_dict['exceptions']['traceback'].append(traceback)

            return False

    def undo(self, workflow_dict):
        LOG.info("Running undo...")
        try:

            return True
        except Exception:
            traceback = full_stack()

            workflow_dict['exceptions']['error_codes'].append(DBAAS_0020)
            workflow_dict['exceptions']['traceback'].append(traceback)

            return False