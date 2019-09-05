====
Data Transformations for Pacific Symphony data
====

.. code-block:: python
    from data_transformations_ps import Donors, Tickets

    donor_cls = Donors(path='../data/donor/')
    ticket_cls = Tickets(fys=[2018, 2019], path='../data/ticket/')

    donor_cls.data.head()
    ticket_cls.data.head()

More in docs