.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================
Account Bank Statement Line Reconciliation
==========================================

The wizard provides the ability to specify bank statement line when it needed.
The only user from security group "Settings" can use it.

Configuration
=============

No additional configuration required

Usage
=====

This module is for you if you work on Odoo enterprise and if messed up the bank reconcile report.

The bank reconciliation report is accessible from the hyperlink 'Difference' which apprears on bank journals cards when the GL balance differs from the bank statement balance.

There are 2 SQL requests launched from field filter (from bank reconcile view) :

1 - Blue lines appears if account_move_lines have these values:

statement_id = false
AND payment_id = true
AND account_id = current bank
-> This means that if you post a payment journal entry manually (meaning that you do not use the register payment button) the payment_id will not be populated then your entry will not be "match-able" → your are stuck -> so you need this module

Same issue in case of migration of payment entries with no payment_id


2 - If 1st request is not applicable then Odoo will look up for account_move_lines with:

reconcile_id = false
account_id = flagged as 'Allow reconciliation" = true
excluding the line in the move with the bank account.
-> This means that is you have created entries on a reconciliable account but you never reconcile it (ie: a cut-off entry or a correction) this line will appear for ever in the list of possible match-> so you may need this module to clean it up.



To use this module, you need to:

#. Go to Accounting > Adviser > Journal Entries
#. Select one or more Journal Entry items
#. Press 'Action > Bank reconcile report change'
#. Select required value in 'New value' field. Leave empty if you want to set empty value.
#. Press 'Set value'

Doing this, you will create/delete the link between Journal entry and bank statement lines so will make do corrctions on the bank reconcile report that would be impossible to do through the Odoo interface.



.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/91/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/account-financial-reporting/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted it
first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Camptocamp SA

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
