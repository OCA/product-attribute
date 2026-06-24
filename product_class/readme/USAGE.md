## Usage

### 1. Create a Product Class

**Navigation:** Inventory → Configuration → Product Classes (or Sales → Configuration → Product Classes)

1. Click **Create** button
2. Enter a **Product Class Name** (e.g., "Chairs")
3. In the **Attributes** section:
   - Click **Add a line**
   - Select an **Attribute** from the dropdown
   - Check **Required** if products of this class must define this attribute
   - Repeat to add more attributes

4. Click **Save**

**Example: "Furniture" Class**

| Attribute  | Required | Notes                               |
|------------|----------|-------------------------------------|
| Color      | ✓        | All furniture must have a color     |
| Size       | ✓        | Sizes vary by product               |
| Material   |          | Optional (not all items specify)    |
| Finish     |          | Optional polish/coating             |

### 2. Assign a Product to a Class

**Navigation:** Inventory → Products → Products

1. Create or edit a product
2. Find the **Product Class** field in the Attributes & Variants tab (added by this module)
3. Select the class (e.g., "Furniture")
4. The form will now restrict **Attributes** to only those allowed by the class

### 3. Add Attribute Lines to a Classed Product

Once a class is selected, you can add attribute lines:

1. Go to the **Attributes & Variants** tab
2. In **Attribute Lines**, click **Add a line**
3. The **Attribute** field dropdown is now filtered to show only class-allowed attributes
4. Select an attribute and provide values
5. **Validation will fail if:**
   - You select an attribute not in the class → Error: "has attribute lines that do not belong"
   - You leave out a required attribute → Error: "is missing required attributes"

### 4. Remove an Attribute from a Class

**Scenario:** Your "Furniture" class allowed "Color" but wants to retire it.

1. Navigate to the class
2. In **Attributes**, find the "Color" line and delete it
3. **Odoo will raise an error if products in this class still use Color**
   - Fix: Remove Color from all products in the class first, then retry the class update

### Workflow Example

**Step 1: Set Up "Chairs" Class**
- Color (required)
- Size (required)
- Leg Material (optional)

**Step 2: Create a "Wooden Chair" Product**
- Assign class: "Chairs"
- Add attribute "Color" = Red (satisfies required)
- Add attribute "Size" = Large (satisfies required)
- Add attribute "Leg Material" = Oak (optional, still valid)
- **Save** ✓ Success

**Step 3: Try Invalid Assignment**
- Assign class: "Chairs"
- Add attribute "Color" = Blue (satisfies required)
- **Try to save without Size** → Error: "is missing required attributes for the selected class 'Chairs': Size"
- Add Size = Medium
- **Save** ✓ Success

### Class Attribute Line Model

The bridge model `product.class.attribute.line` stores:

| Field       | Type      | Purpose                                |
|-------------|-----------|----------------------------------------|
| class_id    | Many2one  | Product class (required, cascade delete)|
| attribute_id| Many2one  | Product attribute (required)           |
| required    | Boolean   | If true, products must define it       |

**Constraint:** A class cannot configure the same attribute twice (unique on class_id + attribute_id).

### Constraints & Validations

1. **Class Constraint** (`_check_attribute_ids_used_by_products`)
   - Prevents removing an attribute from a class if products still use it
   - Error: "Cannot remove attributes used in products assigned to class..."

2. **Product Constraint** (`_check_class_attributes`)
   - Ensures all attribute lines belong to the class
   - Ensures all required attributes are defined
   - Error: "Product '...' has attribute lines that do not belong to the selected class '...'"
   - Error: "Product '...' is missing required attributes for the selected class '...'"

### Advanced: Access Control

- **User (base.group_user):** Can create/read/write product classes and their attributes
- **System/Admin (base.group_system):** Full CRUD including delete

Product class attribute lines follow the same access rules.
