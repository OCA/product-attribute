Sometimes you would like to create product variants based on other model values. 

For example you have a "T-Shirt" product in which two attributes are used among others: "design" and "material".

At the same time you store information about both of them in your db in the dedicated models.

"Design" model keeps the information about image print name, image print category, image author and stores the image file.

"Material" model keeps the information about material name, material type (synthetic/natural), material density and stores a handling instruction in pdf.

Using the regular Odoo flow one will need to create attributes for design and materials and then add values to them.

Eg "Material: cotton, silk, wool", "Design: Fancy Clown, Doge, Pepe, See beach"

And also add the same records to the "Materials" and "Design" models.