from cement.core.handler import Handler
from . import gyb_interface
from cement import shell
import sys

class GYBHandler(gyb_interface.GYBHandler):
    class Meta:
        label = 'gyb_shell'
        interface = 'gyb'

    def actions(self, action=None, email=None, **kwargs):
        # implimented actions: backup, restore, restore-group, estimate, check-service-account
        command = 'gyb --action ' + action + " --email " + email
        for key, value in kwargs.items():
            if key == 'config_folder':
                command += " --config-folder " + value
            if key == 'memory_limit':
                command += ' --memory-limit ' + str(value)
            if key == 'local_folder':
                command += ' --local-folder ' + value

        if action == 'backup' or action == 'restore' or action == 'restore-group':
            command += " --service-account"
            # Sometimes there are minor network issues. Try to rerun the backups 3 times
            runs = 0
            while runs < 3:
                self.app.log.info("gyb action " + action + " For email: " + " Pass: " + str(runs + 1))

                out, err, code = shell.cmd(command, capture=True)
                runs += 1
            
                if code != 0:
                    self.app.log.info('Error running ' + command)
                    self.app.log.debug("Error code: " + str(code)) 
                    self.app.log.debug("\n Standard Out: " + out.decode('utf-8') + "\n Stanard Error: " + err.decode('utf-8'))
                    if runs > 3:
                        sys.exit()
                else:
                    return True
        if action == 'estimate':
            command += " --service-account"
            self.app.log.info("gyb action " + action + " Estimating email size for " + email)
            out, err, code = shell.cmd(command, capture=True)
            if code != 0:
                self.app.log.error("GYB exited with code " + str(code))
                self.app.log.error("Error: " + str(err))
            else:
                return out.decode('utf-8').split("\r")[-2]
        if action == 'check-service-account':
            self.app.log.info("gyb action " + action)

            out, err, code = shell.cmd(command, capture=True)

            if code == 3:
                self.app.log.error('Service account is not setup properly. Contact Senior Tech to setup new client! ')
                self.app.log.debug(out.decode('utf-8'))
                sys.exit()
            elif code != 0:
                self.app.log.error('Error running ' + command)
                self.app.log.debug("Error code: " + str(code)) 
                self.app.log.debug("\n Standard Out: " + out.decode('utf-8') + "\n Stanard Error: " + err.decode('utf-8'))
                sys.exit()
            elif code == 0:
                self.app.log.info("Service Account is setup properly.")
                return True
            else:
                self.app.log.info("Unknown action: " + action)
                sys.exit()
    
    def check_service_account(self, email, config_folder=None):
        # FIXME Need to have a timeout for this. Just rerun it 3 times.
        command = 'gyb --action check-service-account --email ' + email
        
        if config_folder:
            command += ' --config-folder ' + config_folder
        
        self.app.log.info("Testing Service Account. Running 'gyb'")

        out, err, code = shell.cmd(command, capture=True)

        if code == 3:
            self.app.log.error('Service account is not setup properly. Contact Senior Tech to setup new client! ')
            self.app.log.debug(out.decode('utf-8'))
            sys.exit()
        elif code != 0:
            self.app.log.error('Error running ' + command)
            self.app.log.debug("Error code: " + str(code)) 
            self.app.log.debug("\n Standard Out: " + out.decode('utf-8') + "\n Stanard Error: " + err.decode('utf-8'))
            sys.exit()
        elif code == 0:
            self.app.log.info("Service Account is setup properly.")
            return True
    
    def estimat(self, email, config_folder=None, memory_limit=None, local_folder=None):
        command = 'gyb --action estimat --email ' + email
        if config_folder:
            command += ' --config-folder ' + config_folder
        if memory_limit:
            command += ' --memory-limit ' + memory_limit
        if local_folder:
            command += ' --local-folder ' + local_folder

        self.app.log.info("Estimating email size for " + email)
        out, err, code = shell.cmd(command, capture=True)
        if code != 0:
            self.app.log.error("GYB exited with code " + str(code))
            self.app.log.error("Error: " + err)
        else:
            return out.decode('utf-8').split("\r")[-2]

        
    
    def backup(self, email, config_folder=None, memory_limit=None, local_folder=None):
        command = 'gyb --action backup --email ' + email
        if config_folder:
            command += ' --config-folder ' + config_folder
        if memory_limit:
            command += ' --memory-limit ' + memory_limit
        if local_folder:
            command += ' --local-folder ' + local_folder

        self.app.log.info("Backing up " + email)

        # Sometimes there are minor network issues. Try to rerun the backups 3 times
        runs = 0
        while runs >= 3:
            self.app.log.info("Running backup job. Pass: " + str(runs + 1))

            out, err, code = shell.cmd(command, capture=True)
            runs += 1
         
            if code != 0:
                self.app.log.info('Error running ' + command)
                self.app.log.debug("Error code: " + str(code)) 
                self.app.log.debug("\n Standard Out: " + out.decode('utf-8') + "\n Stanard Error: " + err.decode('utf-8'))
                if runs > 3:
                    sys.exit()
            else:
                return True

    def restore(self, email, config_folder=None, memory_limit=None, local_folder=None):
        command = 'gyb --action restore --email ' + email
        if config_folder:
            command += ' --config-folder ' + config_folder
        if memory_limit:
            command += ' --memory-limit ' + memory_limit
        if local_folder:
            command += ' --local-folder ' + local_folder

        # Sometimes there are minor network issues. Try to rerun the job 3 times
        runs = 0
        while runs >= 3:
            self.app.log.info("Running Restore job. Pass: " + str(runs + 1))
            
            out, err, code = shell.cmd(command, capture=True)
            runs += 1
         
            if code != 0:
                self.app.log.info('Error running ' + command)
                self.app.log.debug("Error code: " + str(code)) 
                self.app.log.debug("\n Standard Out: " + out.decode('utf-8') + "\n Stanard Error: " + err.decode('utf-8'))
                if runs > 3:
                    sys.exit()
            else:
                return True

def restore_group(self, email, config_folder=None, memory_limit=None, local_folder=None):
        command = 'gyb --action restore-group --email ' + email
        if config_folder:
            command += ' --config-folder ' + config_folder
        if memory_limit:
            command += ' --memory-limit ' + memory_limit
        if local_folder:
            command += ' --local-folder ' + local_folder

        # Sometimes there are minor network issues. Try to rerun the job 3 times
        runs = 0
        while runs >= 3:
            self.app.log.info("Running Restore job. Pass: " + str(runs + 1))
            
            out, err, code = shell.cmd(command, capture=True)
            runs += 1
         
            if code != 0:
                self.app.log.info('Error running ' + command)
                self.app.log.debug("Error code: " + str(code)) 
                self.app.log.debug("\n Standard Out: " + out.decode('utf-8') + "\n Stanard Error: " + err.decode('utf-8'))
                if runs > 3:
                    sys.exit()
            else:
                return True

def load(app):
    app.handler.register(GYBHandler)


# email=None

# action=None
#     
# ------------

# search=None
# local_folder=None
# label-restored=None
# label-prefix
# strip-labels
# vault
# service_account=False
# use-admin USE_ADMIN
# spam-trash
# batch-size=None
#     {1 - 100}
# noresume
# fast-incremental
# debug
# memory_limit=None
# tls-min-version
# tls-max-version
# ca-file CA_FILE
# extra-reserved-labels
# extra-system-labels
# config_folder=None
# cleanup
# cleanup-date CLEANUP_DATE
# cleanup-from CLEANUP_FROM
