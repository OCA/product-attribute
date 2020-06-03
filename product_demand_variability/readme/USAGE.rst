Firstly, a variability profile must be created.

*   Go to *Inventory>Configuration>Demand Variability>Variability Profile* and
    create a variability profile: select a name, a data source and horizon in
    days past-looking. Finally select the variability profile classes that belong
    to this variability profile.

*   To create a variability profile class, go to
    *Inventory>Configuration>Demand Variability>Variability Profile Classes*.
    Create a class with a lower range and upper range.


After that go to a product and in the "Sales" tab, we can select a
Variability Profile for that product. Additionaly, once the cron has run, we
will be able to see the variability factor of that product, as well as at
which profile variability class it belongs, depending on the variability
profile selected.
