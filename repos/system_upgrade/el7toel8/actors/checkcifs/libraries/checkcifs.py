from leapp import reporting
from leapp.reporting import create_report


def checkcifs(storage_info):
    for storage in storage_info:
        if any(entry.fs_vfstype == "cifs" for entry in storage.fstab):
            create_report([
                reporting.Title("Use of CIFS detected. Upgrade can't proceed"),
                reporting.Summary("CIFS is currently not supported by the inplace upgrade."),
                reporting.Severity(reporting.Severity.HIGH),
                reporting.Groups([
                        reporting.Groups.FILESYSTEM,
                        reporting.Groups.NETWORK
                ]),
                reporting.Remediation(hint='Comment out CIFS entries to proceed with the upgrade.'),
                reporting.Groups([reporting.Groups.INHIBITOR]),
                reporting.RelatedResource('file', '/etc/fstab')
            ])
