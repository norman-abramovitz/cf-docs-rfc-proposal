| Activity | Admin | Admin Read-Only | Global Auditor | Org Manager | Org Auditor | Org Billing Manager | Org User | Space Manager | Space Developer | Space Auditor | Space Supporter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Scope of operation | Org | Org | Org | Org | Org | Org | Org | Space | Space | Space | Space |
| Assign user roles | Yes |  |  | Yes |  |  |  | Yes |  |  |  |
| View users and roles | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Create and assign org quota plans | Yes |  |  |  |  |  |  |  |  |  |  |
| View org quota plans | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Create orgs | Yes |  |  | ^1^ | ^1^ | ^1^ | ^1^ | ^1^ | ^1^ | ^1^ | ^1^ |
| View all orgs | Yes | Yes | Yes |  |  |  |  |  |  |  |  |
| View orgs where user is member | Yes^2^ | Yes^2^ | Yes^2^ | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Edit, rename, and delete orgs | Yes |  |  | Yes^3^ |  |  |  |  |  |  |  |
| Suspend or activate an org | Yes |  |  |  |  |  |  |  |  |  |  |
| Suspend or activate a space | Yes |  |  | Yes |  |  |  |  |  |  |  |
| Create and assign space quota plans | Yes |  |  | Yes |  |  |  |  |  |  |  |
| Create spaces | Yes |  |  | Yes |  |  |  |  |  |  |  |
| View spaces | Yes | Yes | Yes | Yes |  |  |  | Yes | Yes | Yes | Yes |
| Edit spaces | Yes |  |  | Yes |  |  |  | Yes |  |  |  |
| Delete spaces | Yes |  |  | Yes |  |  |  |  |  |  |  |
| Rename spaces | Yes |  |  | Yes |  |  |  | Yes |  |  |  |
| View the status, number of instances, service bindings, and resource use of apps | Yes | Yes | Yes | Yes |  |  |  | Yes | Yes | Yes | Yes |
| Add private domains^4^ | Yes |  |  | Yes |  |  |  |  |  |  |  |
| Share private domains with other orgs | Yes |  |  | Yes^5^ |  |  |  |  |  |  |  |
| Deploy, run, and manage apps | Yes |  |  |  |  |  |  |  | Yes |  | Limited^9^ |
| View app logs | Yes | Yes | Yes | Yes |  |  |  | Yes | Yes | Yes | Yes |
| Use app SSH^6^ | Yes |  |  |  |  |  |  |  | Yes |  |  |
| Instantiate services | Yes |  |  |  |  |  |  |  | Yes |  |  |
| Bind services to apps | Yes |  |  |  |  |  |  |  | Yes |  | Yes |
| Manage global service brokers | Yes |  |  |  |  |  |  |  |  |  |  |
| Manage space-scoped service brokers | Yes |  |  |  |  |  |  |  | Yes |  |  |
| Associate routes^4^, modify resource allocation of apps | Yes |  |  |  |  |  |  |  | Yes |  | Yes |
| Rename apps | Yes |  |  |  |  |  |  |  | Yes |  |  |
| Create and manage Application Security Groups | Yes |  |  |  |  |  |  |  |  |  |  |
| Manage Application Security Groups for all spaces in an org | Yes |  |  | Yes |  |  |  |  |  |  |  |
| Manage Application Security Groups for an individual space | Yes |  |  |  |  |  |  | Yes |  |  |  |
| Create, update, and delete an isolation segment | Yes |  |  |  |  |  |  |  |  |  |  |
| List all isolation segments for an org | Yes | Yes | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ |
| Entitle or revoke an isolation segment | Yes |  |  |  |  |  |  |  |  |  |  |
| List all orgs entitled to an isolation segment | Yes | Yes | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ | Yes^7^ |
| Assign a default isolation segment to an org | Yes |  |  | Yes |  |  |  |  |  |  |  |
| List and manage isolation segments for spaces | Yes |  |  | Yes |  |  |  |  |  |  |  |
| List entitled isolation segments for a space | Yes | Yes | Yes | Yes |  |  |  | Yes | Yes | Yes | Yes |
| List the isolation segment on which an app runs | Yes | Yes | Yes | Yes |  |  |  | Yes | Yes | Yes | Yes |
| List app and service usage events | Yes | Yes | Yes |  |  |  |  |  | Yes | Yes | Yes |
| Create, delete, and list container-to-container networking policies | Yes |  |  |  |  |  |  |  | Yes^8^ |  |  |

^1^Not by default, unless feature flag `user_org_creation` is set to `true`.

^2^Admin, admin read-only, and global auditor roles do not need to be added as members of orgs or spaces to view resources.

^3^Org Managers can rename their orgs and edit some fields. They cannot delete orgs.

^4^Unless deactivated by feature flags.

^5^The user attempting to share must have permissions in both the source and target orgs.

^6^This assumes that SSH is enabled for the platform, space, and app. For more information, see [SSH Access Control Hierarchy](../devguide/deploy-apps/app-ssh-overview.html#ssh-access-control-hierarchy) in _App SSH Overview_.

^7^Applies only to orgs they belong to.

^8^Space Developers can optionally be granted these permissions. For more information, see [Grant Permissions](../devguide/deploy-apps/cf-networking.html#-grant-permissions) in _Configuring Container-to-Container Networking_.

^9^Cannot create packages or delete resources. For more information, see the [Cloud Controller V3 Documentation](https://v3-apidocs.cloudfoundry.org/).
