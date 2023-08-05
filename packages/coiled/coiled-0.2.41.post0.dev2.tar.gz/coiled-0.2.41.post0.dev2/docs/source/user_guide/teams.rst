=====
Teams
=====

Coiled helps individuals and teams manage their resources, control costs, and
collaborate with one another. Team members can share resources, track usage, and consolidate billing
with anyone else on the same account.

Users and accounts
------------------
When you `sign up for Coiled <https://cloud.coiled.io/login>`_, an account is
automatically created for your user, and the name of the account is the same as
your username. For example, if you sign up with the username ``awesome-dev``,
then the ``awesome-dev`` user is automatically added to an account also named
``awesome-dev``.  

If you want to work with a team of two or more users, you can either:

1. Add other users to your existing account by using the Team page at
   ``cloud.coiled.io/<YOUR-ACCOUNT-NAME>/team``

2. Reach out to us at support@coiled.io to create an additional account to use
   for your team such as ``cloud.coiled.io/<YOUR-COMPANY-NAME>/team``

Taking the screenshot below as an example, note that this user Kris (seen in the
avatar on the top right) is viewing the Team page of the Coiled account (seen in
the dropdown on the left).

.. image:: images/team-management.png
    :width: 100%
    :alt: Coiled team page with three users

Working with other accounts
---------------------------

You can create clusters, software environments, and other resources
from any account of which you are a member.

To see all available accounts,
select your avatar from the top right, then select Profile. The Accounts
section is at the bottom of the page. In the example below, user ``sarah-johnson``
is a user on both the ``sarah-johnson`` account and the ``sarahs-team`` account.

.. figure:: images/team-account.png
    :scale: 75%
    :align: center
    :alt: This user has access to the sarah-johnson and the sarahs-team accounts.

In this example, the default account is ``sarah-johnson``. You
can change the account by using the ``account`` keyword argument
commonly accepted in :doc:`API commands <api>` or by specifying
``my-team-name/`` as a prefix in the ``name`` keyword argument.

.. note::
    Once you are added to an account, you can use the cloud provider resources and credentials that have already been setup for your team. Additionally, any tokens you've created will work for any account to which you belong (there is no need to create a new token).

For example, if ``sarah-johnson`` wants to create a cluster in ``sarahs-team``:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(n_workers=5, account="sarahs-team")

Or create a software environment:

.. code-block:: python

   import coiled

   coiled.create_software_environment(
       name="sarahs-team/my-pip-env",
       pip=["dask[complete]", "xarray==0.15.1", "numba"],
   )

You can also configure the default account
using the :doc:`local coiled configuration file <configuration>`.

Sharing software environments
-----------------------------

Software environments which belong to an account are
visible and accessible to all account members. This allows team members to
easily control, share, and collaborate on their teams's resources.

Tracking team resources
-----------------------

Administrators for each Coiled account can set resource limits for account
members like the number of cores a user can allocate at one time or whether or
not to grant access to GPUs (which can be expensive). Additionally, you can
track each cluster's cost over time.

.. image:: images/clusters-table.png
    :width: 100%
    :alt: Cluster usage across different users in the Coiled team.

Visibility into team spending
-----------------------------

Under the billing section (only visible and accessible by account admins), you 
can see more detailed information on account usage, such as your credit 
balance, credits used, and percentage of free credits used.

If you have added a credit card to your account, you will also have visibility
into your Coiled bill for the month:

.. image:: images/month-bill.png
    :width: 100%
    :alt: Month bill table for pay-as-you-go customers

If your usage stays below the amount of free credits, then this value will
always show $0 since you don't have to pay Coiled anything.

Setting a spend limit
^^^^^^^^^^^^^^^^^^^^^

By default, your Coiled account doesn't have a spend limit. You can set a monthly spend limit to ensure your Coiled bill will not exceed the maximum specified value by prohibiting all users in the account from creating new clusters.

.. figure:: images/spend-limit.png
    :scale: 70%
    :align: center
    :alt: Setting spend limit

You can choose whether to shut down already running clusters once the spend limit is reached by selecting **Shut down running clusters if spend limit reached** on the billing page. By default, this box is left unchecked, so as to not automatically interfere with any long-running computations.
