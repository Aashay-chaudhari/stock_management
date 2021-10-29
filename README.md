# Stock Management

A stock management application i created for KrushiArk Naturals and was later sold as an independent stock management software. It is a web application based on django framework in python. The features of this project are listed below :
1) Provides an admin user interface to execute all CRUD operations on all models registered on admin site. Every operation done by Admin is also tracked.
2) Provides intuitive user interface for a user to manage his stock management requirements namely:
      **-> Adding New Product**
      -> Showing previous Purchases/Sales of a particular product
      -> Edit Product
      -> Deleting Product
      **-> Adding New Supplier**
      -> Showing previous Purchases/Sales by a particular Supplier
      -> Edit Supplier
      -> Deleting Product
      **-> Adding New Customer**
      -> Showing previous Purchases/Sales by a particular Customer
      -> Edit Customer
      -> Deleting Product
      **-> Adding a Sales Invoice** 
      -> Printing a Sales Invoice
      -> Edit a Sales Invoice
      -> Deleting a Sales Invoice
      **-> Adding a Purchase Invoice**
      -> Printing a Purchase Invoice
      -> Edit a Purchase Invoice
      -> Deleting a Purchase Invoice
 3) Doesn't allow user to delete Customers/Suppliers if the customer/supplier are linked to any invoice. Shows an error and procedure to follow to obtain this.
 4) Tracks Reorder Levels and throws error on product stock reaching it's reorder level.
