Installing the module changes nothing on its own: internal users are
put in the "Allow duplicate lot/serial numbers" group.

Configuring the module means taking that group away from the users who
should not be allowed to assign duplicate numbers:
Settings \> Users & Companies \> Users

For those users the check then applies to every lot or serial number,
whether it was typed by hand or produced by a sequence.

Existing duplicates are left alone. Only records created or renamed
afterwards are checked.
