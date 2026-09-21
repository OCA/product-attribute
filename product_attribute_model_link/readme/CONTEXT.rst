Sometimes you would like to create a product variant attribute based on other model values.

For example you want to add the Country Of Origin. Instead of creating the whole list of countries in attribute values, why not re-use the countries list already built in Odoo ? It is as simple as linking the Country Of Origin attribute to the Country model and selecting the Country Name field to populate the attribute values.

Here's a more complex use case: you have a "T-Shirt" product in which two attributes are used among others: "design" and "material". At the same time you store information about both of them in your db in the dedicated models.

- "Design" model keeps the information about image print name, image print category, image author and stores the image file.

- "Material" model keeps the information about material name, material type (synthetic/natural), material density and stores a handling instruction in pdf.

Using the regular Odoo flow one will need to create attributes for design and materials and then add values to them. Eg "Material: cotton, silk, wool", "Design: Fancy Clown, Doge, Pepe, See beach". And also add the same records to the "Materials" and "Design" models.
