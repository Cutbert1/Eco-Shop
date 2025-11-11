# Eco | Shop
## Introduction
#### Project Description
This is a local eco-friendly natural products online shop, specialised in selling home/hand made natural products focused on alternative sustainable products, ranging from household products to beauty products. 
#### Project Purpose
The main purpose of the project is create, motivate and  change households behaviours of using non sustainable products which are harmful to our environment and eco system in general. Making green products a household brand and easily accessible, by providing a cheap sustainable alternative to every day products used at home.
#### User Demographic
User demography includes everyone, but most importantly individuals who are keen about green products and want to contribute their quoter in saving our environment from global warming. Marketing strategy, is also aimed at getting more people to become eco-friendly in choosing product they use.

# Eco-Shop Application Wireframe
**Eco-Shop** is a sustainable e-commerce platform selling natural and eco-friendly products with integrated payment processing, user authentication, and comprehensive order management.
## **Site Architecture**

### **Main Navigation Structure**

[header](/static/images/wireframe/header.jpg)

### **Footer Structure**

[footer](/static/images/wireframe/footer.jpg)

## **Page Wireframes**

### **1. HOME PAGE**

[homepage](/static/images/wireframe/homepage.jpg)

### **2. PRODUCTS PAGE** (`/products/`)

[product-page](/static/images/wireframe/product-page.jpg)

### **3. PRODUCT DETAIL PAGE** (`/products/<id>/`)

[product-detail-page](/static/images/wireframe/product-detail-page.jpg)

### **4. SHOPPING BASKET PAGE** (`/basket/`)

[shopping-basket-page](/static/images/wireframe/shopping-basket-page.jpg)

### **5. CHECKOUT PAGE** (`/checkout/`)

[checkout-page](/static/images/wireframe/checkout-page.jpg)

### **6. CHECKOUT SUCCESS PAGE** (`/checkout/checkout_complete/<order_number>/`)

[checkout-auccess-page](/static/images/wireframe/checkout-success-page.jpg)

### **7. USER PROFILE PAGE** (`/profile/`)

[profile-page](/static/images/wireframe/profile-page.jpg)

### **8. AUTHENTICATION PAGES**

[authentication-page](/static/images/wireframe/authentication-page.jpg)

#### **Registration Page** (`/accounts/signup/`)

[registration-page](/static/images/wireframe/regiatration-page.jpg)

### **9. ADMIN PRODUCT MANAGEMENT**

[admin-product-mgt](/static/images/wireframe/admin-product-mgt.jpg)

### **10. INFORMATIONAL PAGES**

#### **Terms & Conditions** (`/terms/`)

[terms-and-conditions](/static/images/wireframe/terms-and=conditions.jpg)

## **Design System**

### **Color Scheme**
- **Primary Green**: Eco-friendly theme
- **Secondary Gray**: Professional contrast  
- **Success Green**: Positive actions
- **Warning Yellow**: Stock alerts
- **Danger Red**: Critical actions
- **Light Gray**: Backgrounds

### **Typography**
- **Headers**: Bold, modern sans-serif
- **Body Text**: Clean, readable font
- **Buttons**: Uppercase, rounded corners
- **Icons**: Font Awesome integration

### **Interactive Elements**
- **Hover Effects**: Smooth transitions
- **Buttons**: Pill-shaped with shadows
- **Cards**: Subtle shadows with hover lifts
- **Forms**: Clean inputs with validation

## **Responsive Design**

### **Mobile First Approach**
- **Product Grid**: 1-2 columns on mobile, 4 on desktop
- **Navigation**: Collapsible hamburger menu
- **Touch Targets**: Minimum 44px tap areas
- **Simplified Layouts**: Stacked content on mobile

### **Tablet Optimization**
- **3-column product grids**
- **Sidebar layouts** for forms
- **Touch-friendly controls**

### **Desktop Enhancement**
- **4-column product grids**
- **Hover interactions**
- **Keyboard navigation**
- **Large click targets**

## **Technical Features**

### **Performance**
- **Image optimization** with lazy loading
- **CDN integration** (AWS S3)
- **Caching strategies**
- **Scroll-to-top** buttons

### **Accessibility**
- **ARIA labels** for screen readers
- **Keyboard navigation** support
- **Color contrast** compliance
- **Alt text** for all images

### **Security**
- **CSRF protection** on all forms
- **User authentication** (Django Allauth)
- **Admin-only** product management

# **E-commerce Features**

### **Shopping Experience**
- **Real-time inventory** checking
- **Quantity validation** with alerts
- **Stock status** badges
- **Related products** suggestions

### **Payment Processing**
- **Stripe integration**
- **Secure checkout** forms
- **Order confirmation** emails
- **Delivery estimates**

### **User Management**
- **Profile management**
- **Order history**
- **Delivery address** saving
- **Email verification**

## **Admin Features**

### **Product Management**
- **Add/Edit/Delete** products
- **Category management**
- **Inventory tracking**
- **Image uploads**

### **Order Management**
- **Order processing**
- **Status updates**
- **Customer communication**
- **Sales reporting**

## **Entity Relationship Diagram (ERD)**

### **Database Schema Overview**
The Eco-Shop application uses a relational database with the following key entities and relationships:

[db-schema](/static/images/wireframe/db-schema.jpg)
### **Detailed Entity Descriptions**

#### **1. User (Django Built-in)**
- **Purpose**: Django's built-in authentication system
- **Key Fields**: username, email, password, staff status
- **Relationships**: One-to-One with AccountProfile

#### **2. AccountProfile**
- **Purpose**: Extended user profile with delivery information
- **Key Fields**: Contact details, primary address, timestamps
- **Relationships**: 
  - One-to-One with User
  - One-to-Many with Order

#### **3. Category**
- **Purpose**: Product organization and navigation
- **Key Fields**: name, slug (for URLs), description, icon, display order
- **Relationships**: One-to-Many with Product
- **Features**: Auto-generated slugs, hierarchical ordering

#### **4. Product**
- **Purpose**: Core product catalog with inventory management
- **Key Fields**: 
  - Basic info: name, brand, SKU, descriptions, price, rating
  - Inventory: count, threshold, active status, digital flag
  - Physical: weight, images
  - Timestamps: created_on, updated_on
- **Relationships**: 
  - Many-to-One with Category
  - Many-to-Many with Order (through OrderLineItem)
- **Methods**: Stock checking, delivery estimation, inventory adjustment

#### **5. Order**
- **Purpose**: Customer purchase records with payment tracking
- **Key Fields**: 
  - Identity: order_number (UUID), customer details
  - Address: Full delivery address with country
  - Financial: totals, delivery cost, Stripe payment ID
  - Status: order_status, payment_status, delivery_eta
  - Metadata: timestamps, basket snapshot, delivery notes
- **Relationships**: 
  - Many-to-One with AccountProfile
  - One-to-Many with OrderLineItem
- **Enums**: OrderStatus (pending/processing/completed/cancelled)
          PaymentStatus (awaiting/paid/failed)

#### **6. OrderLineItem**
- **Purpose**: Individual products within an order
- **Key Fields**: quantity, unit_price, lineitem_total
- **Relationships**: 
  - Many-to-One with Order
  - Many-to-One with Product
- **Business Logic**: Auto-calculates totals, manages inventory

### **Key Relationships & Business Rules**

#### **User Management**

User ←→ AccountProfile (1:1)
├── Automatic profile creation via Django signals
├── Stores delivery preferences and contact info
└── Links to order history

#### **Product Catalog**

Category ←→ Product (1:M)
├── Products can have zero or one category
├── Categories organize navigation and filtering
├── Slug-based URLs for SEO
└── Hierarchical ordering system

#### **Order Processing**

AccountProfile ←→ Order (1:M)
├── Guest orders possible (null account_profile)
├── Order status workflow: pending → processing → completed
├── Payment integration with Stripe
└── Automatic delivery estimation

#### **Order Items**

Order ←→ OrderLineItem ←→ Product (M:M through relationship)
├── Each line item links one product to one order
├── Captures price at time of purchase (unit_price)
├── Automatic inventory adjustment on save/delete
└── Calculates line totals and updates order totals

### **Database Constraints & Validations**

#### **Unique Constraints**
- `Product.name`: Unique product names
- `Product.sku`: Unique stock keeping units
- `Category.slug`: Unique URL slugs
- `Order.order_number`: Unique order identifiers

#### **Foreign Key Behaviors**
- `Product.category`: SET_NULL (products remain when category deleted)
- `Order.account_profile`: SET_NULL (orders remain for deleted users)
- `OrderLineItem.order`: CASCADE (line items deleted with order)
- `OrderLineItem.product`: CASCADE (prevents product deletion with orders)

#### **Business Logic Constraints**
- Inventory tracking disabled for digital products
- Order totals auto-calculated from line items
- Payment status linked to order status transitions
- Delivery estimates based on product types

## Features
### Existing Features
### Home page
This is the landing page which follows the theme of green background with happy shoppers and several buttons to navigate the site.

![homepage](/static/images/readme_images/features_images/homepage.jpg)
### Logo
This is the eco | Shop logo that takes you to the landing page when clocked from anywhere on the website

![logo](/static/images/readme_images/features_images/logo.jpg)
### Navbar
This is the navigation section of all products categories, search, accounts and basket. It also includes filters for deals and clearance.

![navbar-desktop](/static/images/readme_images/features_images/navbar-desktop.jpg)

![navbar-mibile](/static/images/readme_images/features_images/navbar-mobile.jpg)
### Products page
This is the page where all the products are delayed, with images, names, amount, category and ratings.

![products](/static/images/readme_images/features_images/products.jpg)
### Product Details Page
This is a page that provide full details of individual product and give you the ability to add to basket or continue shopping. As a super user you can also update or delete product through this page.

![product-details](/static/images/readme_images/features_images/product-details.jpg)

### Add Product Page (Product Management)
This is the page were only a super user can access to add products.

![product-management](/static/images/readme_images/features_images/product-management.jpg)
### Update Product Page
This is the page were only a super user can access to make changes to a products.
![update-product1](/static/images/readme_images/features_images/update-product1.jpg)
![update-product2](/static/images/readme_images/features_images/update-product2.jpg)
### Basket Page
This page tallies up all your items, provide you with ability to add more quantity, reduce quantity or remove item completely from your basket. You can go to secure checkout from this page or continue shopping.

![basket](/static/images/readme_images/features_images/basket.jpg)
### Checkout Page
This is the page were you fill your Billing and shipping details, provide debit or credit card details. Your order summary and charges are also provided on this page. You can update your basket from this page or complete your order.

![checkout1](/static/images/readme_images/features_images/checkout1.jpg)

![checkoit2](/static/images/readme_images/features_images/checkout2.jpg)
### Chekout Complete Page
This page is rendered when order is completed, stating your order  details, order number, product name and charges incurred. You can also check out special offers from this page.
![checkout-complete1](/static/images/readme_images/features_images/checkout-complete1.jpg)
![checkout-complete2](/static/images/readme_images/features_images/checkout-complete2.jpg)

### Confirmation Email
Once order is successful and saved in database, a confirmation email is sent to user.

![confirmation-email](/static/images/readme_images/features_images/confirmation-email.jpg)
### Signup Page
Page is used to become a registered member of eco shop.

![signup](/static/images/readme_images/features_images/signup.jpg)
### Login Page
Page used by registered members to sign into eco shop.

![signin](/static/images/readme_images/features_images/signin.jpg)
### Logout Page
This page is used to logout from the site.

![logout](/static/images/readme_images/features_images/logout.jpg)
### Toast
Used to display information on status of user actions. It also display success messge with details of items added to basket.

![product-details1](/static/images/readme_images/features_images/product-details1.jpg)

![toast-success](/static/images/readme_images/features_images/toast-success.jpg)

![toast-error](/static/images/readme_images/features_images/toast-error.jpg)

![toast-info](/static/images/readme_images/features_images/toast-info.jpg)
### Profile Page
Page to update personal profile, which can be used for future checkout form completions for registered users. Profile page all displays user order history.

![profile](/static/images/readme_images/features_images/profile.jpg)
### Footer and Social Network Icons
Footer that displays links to access social media pages for eco shop.

![footer](/static/images/readme_images/features_images/footer.jpg)
### Terms, Privacy, FQA, Returns, Our Blog
Renders a new window for Terms, Privacy, FQA, Returns, Our Blog.

![footer-links](/static/images/readme_images/features_images/footer-links.jpg)

## Future Improvements
* Add a loading overlay with a  spinner at the centre of the screen indicating payment is being processed.
* Add wish list container for registered users 
* Add points and rewards for registered, frequent customers
* Add products review comment section
## E-commerce business model.
### Business model B2C(Business-to-Consumer)
The business model chosen for this project is B2C. Before choosing this business model 3 key questions were answered.
|Who is the customer| What will they buy | How will they pay |
|:------------|:----------------|:--------------|
|Decides to buy on their own|Sustainable alternative products|Single Payment|
|Keen on Green products|Sustainable alternative products|Single Payment|
|Inpulsive buyers|Sustainable alternative products|Single Payment|
|Easy payment system without hassle|Sustainable alternative products|Single Payment|

With these questions answered, a consideration of the features of the application  that aligns with above answers was considered.
#### What will they buy (Products)
|Application Features| 
|:------------|
|Product Search|
|Filter Categories|
|Add Products|
|Update Products|
|Show Products Count|
|User Profile|
|Order Notification|
|Authentication System|
|Basket and Payment System|

|Application Database|
|:------------|
|Product Images|
|Product Name|
|Product Description|
|Delivery Cost|
|Shipping Details|
|Product Ratings|

#### How will they pay (Single Payment)
|Singel Payment|
|:------------|
|Easy Payment without hassle|
|Transaction must be finished after each single payment|
|Payment refund or product return for unsatisfied customer within a specified time-line|

## Marketing Strategies
This project has no budget and having considered pros and cons of all marketing strategies,  key marketing strategies  used are Organic social media marketing, Email marketing and Search engine optimisation.

**Reasons for choosing Organic social media marketing strategy:**
* The business has little or no budget for affiliate marketing and paid advertising.
* As this is an eco-friendly shop we intend to build a brand identity that is recognisable to everyone, especially for green conscious audience. 
* Aim to build loyalty with our customers/ audience through interaction on social media 
* Create and share contents and blogs targeted at green audience .
* Showcases our products to variety of potential customers in different social media platform.
* Gives our customers opportunity to share our contents to other platforms.

**Reasons for choosing Email marketing strategy:**
* Due to lack of budget email marketing was choosen because it is free to set up.
* With large email list eco shop can reach out to large audience at considerably low cost
* Eco shop will have complete design over email correspondence.
* Using email marketing is more likely to convert our subscribed customers to paying customers.
* As a startup, we don't have to be overly consistent to pull in paying customers and we also have the opportunity to test diffrence sections of our newsletter.


## Search Engine Optimization and Ranking
### A short-tail and long tail keywords were formulated
|Short-Tail Keywords|   Long-Tail Keywords   |
|:------------|:----------------|
|Eco|Organically made products|
|Eco Friendly|Healthy Organic products|
|Sustainable products|Alternative green products|
|Natural|Nature friendly products|
|Gogreen|organic beaty products|
|Recycle|Sustainable grooming products|
| |Buy locally sourced organic products|
| |Natural and Sustainable Alternative Products|
| |Organic Sustainable Products|

* These Keywords  were logical embed all through the site avoiding keyword stuffing. 

* Meta tags keywords, and decrtiption were included in base.html template

* Used rel="noopener" for some social media links, hence intructing search engine not to crawl the social media page.

### Sitemap.xml
Generated sitemap.xml, which is incldued to this project. Site map is not expected to work on this project as it not deployed to a custom domain

![sitemap](/static/images/readme_images/features_images/sitemap.jpg)
### Robots.txt
robots.txt was also included to the project detailing links the user-agent should disallow.

![robots](/static/images/readme_images/features_images/robots.jpg)

* Terms and Conditions, FQA, Privay Statements and blogs with external quality site, was added to the site to improve ranking.

## Web Marketing 
### Facebook Page for digital marketing
Facebook business page created for eco | shop

![facebook1](/static/images/readme_images/features_images/facebook1.jpg)

![facebook2](/static/images/readme_images/features_images/facebook2.jpg)

![facebook3](/static/images/readme_images/features_images/facebook3.jpg)

![facebook4](/static/images/readme_images/features_images/facebook4.jpg)

![facebook5](/static/images/readme_images/features_images/facebook5.jpg)
### Newsletter signup form for the purposes of digital marketing.
Create an account with Mailchimp and complete the details requires eg. Business email address and Business address for compliance. On the dashboard select Campaign, Signup form and then embedded form. Give the form a tittle and select the feeds you want the user see and use.
A simple subscription form was created to enable interested users subscribe using mailchimp. Only email field was used to make it easy and quick for users to subscribe.

![email-marketing](/static/images/readme_images/features_images/email-marketing.jpg)
## Manual Testing
### Features Testing
|Key Features|   User Value   |Functionality Test|Outcome|
|:------------|:----------------|:-------------|:------------|
|Logo|Assist user navigate through the website as it renders the Home page when logo is clicked.![logo](/static/images/readme_images/features-testing-images/logo.jpg)|While on any other page (products, product_detail, basket, checkout etc) click on logo.|While on checkout page, logo was clicked and home page was rendered. Facilitates users experience should they want to view our blog, term, FAQ and return policy. ![logo-outcome](/static/images/readme_images/features-testing-images/logo-outcome.jpg)|
|Navbar|Use to transverse all through the site, to search for products, filter by categories, price and ratings. ![navbar](/static/images/readme_images/features-testing-images/navbar.jpg)|From any page any page, click on drop down for any category to select products from sub categories |Clicked on makeup to select  glitters. ![navbar-outcome](/static/images/readme_images/features-testing-images/navbar-outcome.jpg)|
|Product Search|Use for product search, word in product name or description. ![search](/static/images/readme_images/features-testing-images/search.jpg)|Type chosen word in search field and press enter, if word exist products related to the word will render.|Typed “natural” in search field and products with “natural” in there name or description is displayed with product count. ![search-outcome](/static/images/readme_images/features-testing-images/search-outcome.jpg)|
|Filter by Price|Use to filter price in ascending order, from cheapest to most expensive products. This is for all products.|Select “All Products”, then select “By Price”. Page will render products prices in ascending order.|Selected “All Products”, then selected “By Price”. Page renders product prices in ascending order. ![filer-price-outcome](/static/images/readme_images/features-testing-images/filter-price-outcome.jpg)|
|Filter by Rating|Use to filter rating in descending order, from highest to lowest rated products. This is for all products.|Selected “All Products”, then selected “By Rating”. Page renders product ratings in descending order.|Selected “All Products”, then selected “By rating”. Page renders rating in descending order. ![rating-outcome](/static/images/readme_images/features-testing-images/rating-outcome.jpg)|
|Filter by Category|Use to filter products by category name alphabetical order. This is for all products.|Selected “All Products”, then selected “By Category”. Page renders products by category name alphabetical order.|Selected “All Products”, then selected “By Category”. Page renders products by category name alphabetical order. ![category-outcome](/static/images/readme_images/features-testing-images/category-outcome.jpg)|
|Filter by Skincare|Use to filter products by skincare, and chose any sub category of your choice|Select “Skincare”, then select any sub category of your choice. Page renders products of chosen sub category.|Selected “Skincare”, then selected “Deodorants”. Page renders deodorant products in store. ![skincare-outcome](/static/images/readme_images/features-testing-images/skincare-outcome.jpg)|
|Filter by Haircare|Use to filter products by haircare, and chose any sub category your choice.|Select “Haircare”, then select any sub category of your choice. Page renders products of chosen sub category.|Selected “Haircare”, then selected “Conditioners”. Page renders Conditioner products in store. ![haircare-outcome](/static/images/readme_images/features-testing-images/haircare-outcome.jpg)|
|Filter by Makeup|Use to filter products by makeup, and chose any sub category of your choice.|Select “Makeup”, then select any sub category of your choice. Page renders products of chosen sub category.|Selected “Makeup”, then selected “Lips”. Page renders Lips products in store. ![makeup-outcome](/static/images/readme_images/features-testing-images/makeup-outcome.jpg)|
|Filterby Bathroom|Use to filter products by bathroom, and chose any sub category of your choice.|Select “Bathroom”, then select any sub category of your choice. Page renders products of chosen sub category.|Selected “Bathroom”, then selected “Soap Bar”. Page renders Soap Bar products in store. ![bathroom-outcome](/static/images/readme_images/features-testing-images/bathroom-outcome.jpg)|
|Filter by Kitchen|Use to filter products by kitchen, and chose any sub category of your choice.|Select “Kitchen”, then select any sub category of your choice. Page renders products of chosen sub category.|Selected “Kitchen”, then selected “Kitchen Essentials”. Page renders Kitchen Essentials products in store. ![kitchen-essentials-outcome](/static/images/readme_images/features-testing-images/kitchen-essentials-outcome.jpg)|
|Filter by Special Offers|Use to filter products by special offers, and chose any sub category of your choice.|Select “Special Offers”, then select any sub category of your choice. Page renders products of chosen sub category.|Selected “Special Offers”, then selected “Clearance”. Page renders Clearance products in store. ![special-offer-outcome](/static/images/readme_images/features-testing-images/special-offers-outcome.jpg)|
|Sort by Price (low to high)|Use to sort products by price (low to high)|Select “Sort by price (low to high)”, Page renders products with prices in ascending order|Selected “Sort by price (low to high)”,Page renders products starting from lowest priced item. ![sort-price-lh](/static/images/readme_images/features-testing-images/sort-price-lh.jpg)|
|Sort by Price (high to low )|Select “Sort by price (high to low)”, Page renders products with prices in descending order.|Select “Sort by price (high to low)”, Page renders products with prices in descending order.|Selected “Sort by price (high to low)”,Page renders products starting from highest priced item. ![sort-price-hl](/static/images/readme_images/features-testing-images/sort-price-hl.jpg)|
|Sort by Rating (low to high)|Use to sort products by rating (low to high)|Select “Sort by rating (low to high)”, Page renders products with ratings in ascending order.|Selected “Sort by rating (low to high)”,Page renders products starting from lowest rated item. ![ratings-lh](/static/images/readme_images/features-testing-images/ratings-lh.jpg)|
|Sort by Rating (high to low)|Use to sort products by rating (high to low)|Select “Sort by rating (high to low)”, Page renders products with ratings in descending order.|Selected “Sort by rating (high to low)”,Page renders products starting from highest rated item. ![ratings-hl](/static/images/readme_images/features-testing-images/ratings-hl.jpg)|
|Sort by Name (A to Z)|Use to sort products by name (A to Z).|Select “Sort by name (A to Z)”. Page renders products with name in alphabeticalorder.|Selected “Sort by name (A to Z)”. Page renders products starting with name A to Z. ![namea-z-outcome](/static/images/readme_images/features-testing-images/namea-z-outcome.jpg)|
|Sort by Name (Z to A)|Use to sort products by name (Z to A)|Select “Sort by name (Z to A)”. Page renders products with name in reverse alphabeticalorder.|Selected “Sort by name (Z to A)”. Page renders products starting with name Z to A. ![namez-a-outcome](/static/images/readme_images/features-testing-images/namez-a-outcome.jpg)|
|Sort by Category (A to Z)|Use to sort products by category (A to Z)|Select “Sort by category (A to Z)”. Page renders products with category names in alphabetical order|Selected “Sort by category (A to Z)”. Page renders products starting with category name  A to Z. ![categorya-z-outcome](/static/images/readme_images/features-testing-images/categorya-z-outcome.jpg)|
|Sort by Category (Z to A)|Use to sort products by category (Z to A).|Select “Sort by category (Z to A)”. Page renders products with category names in reverse alphabetical order.|Selected “Sort by category (Z to A)”. Page renders products starting with category name  Z to A. ![categoryz-a-outcome](/static/images/readme_images/features-testing-images/categoryz-a-outcome.jpg)|
|Shop all products button|Use to go to main products page were list of products are displayed from the home page.|From the home page click “shop all products” button. ![shop-products](/static/images/readme_images/features-testing-images/shop-products.jpg)|Clicked “shop all products” button. Page renders list of products. ![shop-products-outcome](/static/images/readme_images/features-testing-images/shop-products-outcome.jpg)|
|Clearance and Deals button|Use to see products on clearance and deals directly from the home page|From the home page click "click clearance and deals button. ![clearance-deals](/static/images/readme_images/features-testing-images/clearance-deals.jpg)|Clicked “clearance and deals” button. Page renders special offer products.![clearance-deals-outcome](/static/images/readme_images/features-testing-images/clearance-deals-outcome.jpg)|
|Super User Update product button|Use to update product details as a super user|Select “update” and make changes to any product field of your choice and click “update product”. ![update-product](/static/images/readme_images/features-testing-images/update-product.jpg) ![update-product2](/static/images/readme_images/features-testing-images/update-product2.jpg) |Clicked “update”, made changes to price. From $23.00 to $25 and clicked update product button to save. ![update-product-outcome](/static/images/readme_images/features-testing-images/update-product-outcome.jpg)|
|Super User Delete product button|Use to delete product as a super user|Click delete product button as a super user. ![delete-product](/static/images/readme_images/features-testing-images/delete-product.jpg)|Clicked delete button and product was deleted.|
|Add to basket button|Use to add product to basket|On product details page click add to basket button. ![add-to-basket](/static/images/readme_images/features-testing-images/add-to-basket.jpg)|Clicked “add to basket” button and product was added. ![add-to-basket-outcome](/static/images/readme_images/features-testing-images/add-to-basket-outcome.jpg)|
|Continue Shopping button|Use to navigate  back to product list if you want to continue shopping.|From the product details page click ”continue shopping” button to go back to list of products. ![continue-shopping](/static/images/readme_images/features-testing-images/continue-shopping.jpg)|From the product details page clicked ”continue shopping” button and went back to list of products. ![continue-shopping-outcome](/static/images/readme_images/features-testing-images/continue-shopping-outcome.jpg)|
|Proceed to checkout button|Use to navigate from toast basket to shopping basket|From toast basket click “proceed to checkout”, renders basket page. ![proceed](/static/images/readme_images/features-testing-images/proceed.jpg)|Clicked “proceed to checkout” button from toast basket, basket page is rendered. ![proceed-outcome](/static/images/readme_images/features-testing-images/proceed-outcome.jpg)|
|Secure Checkout Button|Use to navigate from  basket to checkout page|From basket click “secure checkout” button, renders checkout page. ![secure](/static/images/readme_images/features-testing-images/secure.jpg)|Clicked “secure checkout” from basket, checkout page is rendered. ![secure-outcome](/static/images/readme_images/features-testing-images/secure-outcome.jpg)|
|Complete Order button|Use to complete order after payment|On checkout page after payment details click “complete order” renders order complete page. ![complete](/static/images/readme_images/features-testing-images/complete.jpg)|Clicked “complete order” from checkout page, checkout complete page is rendere. ![complete-outcome](/static/images/readme_images/features-testing-images/complete-outcome.jpg)|
|Increase or Decrease Product Qauntity|Use to increase or decrease quantity of item you want purchase|In product details page click “+” or “-“ to increase or decrease quantity of item. ![increase](/static/images/readme_images/features-testing-images/increase.jpg) ![decrease](/static/images/readme_images/features-testing-images/decrease.jpg)|Clicked ““+” or “-“” to increase or decrease quantity of item. Item quantity increased and decreased|
|Update Product button in shopping basket|Use to update product quantity in basket page|click “+” or “-“ to increase or decrease quantity then click "update" to update quantity in basket. ![update-basket](/static/images/readme_images/features-testing-images/update-basket.jpg)|Clicked “+” to increase to 4 quantity then clicked “update” to update quantity in basket. ![update-basket-outcome](/static/images/readme_images/features-testing-images/update-basket-outcome.jpg)|
|Remove Product button in shopping basket|Use to remove item from basket|On basket page, click “remove” to remove item from basket.|Clicked “remove” to remove item from basket. Item removed from basket. ![remove-basket-outcome](/static/images/readme_images/features-testing-images/remove-basket-outcome.jpg)|
|My Account|As a super user, it’s used to add product, create/manage profile and login/logout. As a non-registered user, it is used for registration and login.  As a registered user, it is used for managing profile and logout.|As a super user, clicked on “account” dropdown to create/manage profile and login/logout. ![account](/static/images/readme_images/features-testing-images/account.jpg)As a registered user, clicked on “account” dropdown to manage profile and logout. ![registered](/static/images/readme_images/features-testing-images/registered.jpg) As a non-registered user, clicked on “account” dropdown for registration and login. ![non-registered](/static/images/readme_images/features-testing-images/non-registered.jpg)|Navigate through account dropdown depending on permission|
|Product Management|Use by super user to add products to store|Click on product management, completed the form fields with required details, select product image and click add product. ![product-managament](/static/images/readme_images/features-testing-images/product-management.jpg)|Product added to database and renders product detail page. ![product-management-outcom](/static/images/readme_images/features-testing-images/product-management-outcome.jpg)|
|My Profile|Use to store and update registered user profile|Check “save shipping details to profile” on checkout. Details will be saved on profile and used for any future purchase. ![save-profile](/static/images/readme_images/features-testing-images/save-profile.jpg)|Details saved to profile, with order history. ![save-profile-outcome](/static/images/readme_images/features-testing-images/save-profile-outcome.jpg)|
|Logout|Use to signout of the site|As a logged in user, select account, then logout. ![logout](/static/images/readme_images/features-testing-images/logout.jpg)|Renders sign out page. ![logout-outcome](/static/images/readme_images/features-testing-images/logout-outcome.jpg)|
|Login|Use to log into the site as a registered user|As a registered user, clicked on “account” dropdown to login. ![login](/static/images/readme_images/features-testing-images/login.jpg)|Clicked on “account” dropdown, then login, renders sign-in page. ![login-outcome](/static/images/readme_images/features-testing-images/login-outcome.jpg)|
|Signup|Use to register details on site |As a non-registered user, clicked on “account” dropdown to register|Clicked on “account” dropdown, then register, renders sign-up page. ![signup](/static/images/readme_images/features-testing-images/signup.jpg)|
|Basket|Use to store purchases being made by a user|Select “add to basket” on the product you want to purchase|Selected “add to basket” on the product I want to purchase, basket stored the product details, amount, quantity, name of product etc. ![basket](/static/images/readme_images/features-testing-images/basket.jpg)|
|Checkout form|Use to fill in billing, shipping and payment details.|Complete billing, shipping and payment details, phone number MUST contain country code then click “complete order”. ![checkout-form](/static/images/readme_images/features-testing-images/checkout-form.jpg)|Order processed and checkout complete page rendered with order details. ![checkout-form-outcome](/static/images/readme_images/features-testing-images/checkout-form-outcome.jpg)|
|Webhook payment_intent.succeeded|Used to confirm customer payment|Place an order on the frontend and review webhook events for deployed eco shop checkout/wh/ endpoint [stripe](https://eco-shop-natural-56f100a41f30herokuapp.com/checkout/wh/)|Placed an order and checked [stripe](https://eco-shop-natural-56f100a41f30herokuapp.com/checkout/wh/) for payment_intent.succeeded event. ![payment-intent-succeed](/static/images/readme_images/features-testing-images/payment-intent-succeed.jpg)|
|E-mail Confirmation|Use to confirm order has been processed to the customer|Place an order and email confirmation detailing order info will be sent to your inbox.|Placed an order and confirmation email was sent to my inbox. ![email](/static/images/readme_images/features_images/confirmation-email.jpg)|
|Newsletter signup form.|Use to enable users to subscribe to eco shop, digital marketing. ![newsletter-email](/static/images/readme_images/features_images/newsletter-email.jpg)|Fill your email address and click subscribe. ![newsletter](/static/images/readme_images/features-testing-images/newsletter.jpg) Re-using same email address for subscription will display **"You're already subscribed, your profile has been updated. Thank you!"** ![already-sub](/static/images/readme_images/features_images/already-sub.jpg)|Fill in email address clicked subscribed, check mailchimp account and saw email address added. ![mailchimp](/static/images/readme_images/features_images/mailchimp-subs.jpg)|
|404 page|Use to inform users they are accessing  a URL that does not exist in the application|Change URL to any broken URL path, eg plan|Renderes 404 page. ![404-fix](/static/images/readme_images/features-testing-images/404-fix.jpg)|
|Our Blog external link|Use to access external content to read more from our blog|From “our blog” page click “read more”|From “our blog” page clicked “read more”, renders external content related to topic being discussed on the blog.|
|Terms and Conditions link|Use to access our terms and conditions of service|From the home page footer click "Terms"|Clicked "Terms" and terms and conditions page was rendered|
|Privacy Statement link|Use to access our policy statement|From the home page footer click "Privacy"|Clicked "Privacy" and privacy statment page was rendered|
|Returns link|Use to access our return policy and process|From the home page footer click "Returns"|Clicked "Returns" and return policy and process page was rendered|
|Facebook link|Use to access our Facebook business page|From the home page footer click "facebook icon"|Clicked "facebook icon" and facebook business page was rendered|
|Scroll-to-top-button|Use to scroll to the top of product list page|Click on scroll to get to the top of product list page. ![scroll](/static/images/readme_images/features-testing-images/scroll.jpg)|While at the bottom of product list page, clicked on scroll button to get to the top of the page. Scroll button is not visible when you are at the top of the page|
|Download button for Terms, Privacy and Returns|Use to download Terms, Privacy statement and Return policy to your device|On "Terms page, click on download to get document downloaded to your device. ![download](/static/images/readme_images/features-testing-images/download.jpg)|From "Terms" page clicked download, document downloaded to my device|

### Lighthouse Performance
|View Tested|   Outcome of the audit  |Soulution Applied|Screenshot of clear Validator output|
|:------------|:----------------|:-------------|:------------|
|Moble|![mobile](/static/images/readme_images/lighthouse_test/mobile.jpg)|Unable to apply any solution to improve performance as most are due to external links used for specific functionalities throughout the site. Example, Stripe, AWS, Fontawsom, Bootstrap etc. ![3rd-part-mobile](/static/images/readme_images/lighthouse_test/3rd%20-party-mobile.jpg)|![lighthouse-desktop](/static/images/readme_images/lighthouse_test/desktop.jpg)|
|Desktop|![lighthouse-desktop](/static/images/readme_images/lighthouse_test/desktop.jpg)|Unable to apply any solution to improve performance as most are due to external links used for specific functionalities throughout the site. Example, Stripe, AWS, Fontawsom, Bootstrap etc. ![3rd-party](/static/images/readme_images/lighthouse_test/3rd%20party.jpg)|![lighthouse-desktop](/static/images/readme_images/lighthouse_test/desktop.jpg)|

### Validation Testing
#### HTML Pages [HTML W3C Validator](https://validator.w3.org/)
|Page Tested|Screenshot of Errors and Warnings   |Solution Applied|Screenshot of clear Validation Output|
|:------------|:----------------|:-------------|:------------|
|Home page|![home-page](/static/images/readme_images/validation_testing/homepage.jpg)|Updated unordered list as parent element to list item. Changed ID to avoid duplication between mobile-top-header.html and base.html. Removed trailing slash from mailchimp href.|All error was cleared. There are 2 warnings of possible misuse of aria-label. ![home-page-fix](/static/images/readme_images/validation_testing/homepage-fix.jpg)|
|products page|![product-list-fix](/static/images/readme_images/validation_testing/homepage-fix.jpg)|No error. 2 warnings of aria-label possible misuse |No error. 2 warnings of possible misuse aria-label use. ![product-list-fix](/static/images/readme_images/validation_testing/homepage-fix.jpg)|
|product_detail.html|![product-details](/static/images/readme_images/validation_testing/homepage-fix.jpg)|No error. 2 warnings of aria-label possible misuse |No error. 2 warnings of possible misuse aria-label use.![product-details](/static/images/readme_images/validation_testing/homepage-fix.jpg) |
|basket page|![basket-page](/static/images/readme_images/validation_testing/basket-page.jpg)|Add alt attribute to image. Updated stray div end tag which also resolved the form error|All error was cleared. There are 2 warnings of possible misuse of aria-label. ![basket-page-fix](/static/images/readme_images/validation_testing/homepage-fix.jpg)|
|checkout page|![checkout-page](/static/images/readme_images/validation_testing/homepage-fix.jpg)|No error. 2 warnings of aria-label possible misuse|![checkout-page-fix](/static/images/readme_images/validation_testing/homepage-fix.jpg)|
|checkout_complete.html|![checkout-complete-page](/static/images/readme_images/validation_testing/homepage-fix.jpg)|No error. 2 warnings of aria-label possible misuse|![checkout-complete-page-fix](/static/images/readme_images/validation_testing/homepage-fix.jpg)|
|Blog page|![blog-page](/static/images/readme_images/validation_testing/blog-page.jpg)|Add html boilerplate, updated unclosed div elements|No error or warning. ![blog-page-fix](/static/images/readme_images/validation_testing/blog-page-fix.jpg)|
|FAQ page|![faq-page](/static/images/readme_images/validation_testing/faq-page.jpg)|Add html boilerplate, and moved header to become child to body tag|No error or warning. ![faq-page-fix](/static/images/readme_images/validation_testing/faq-page-fix.jpg)|
|Privacy page|![privacy-page](/static/images/readme_images/validation_testing/privacy-page.jpg)|Add html boilerplate, and moved header to become child to body tag|No error or warning. ![privay-page-fix](/static/images/readme_images/validation_testing/privacy-page-fix.jpg)|
|Terms page|![terms-page](/static/images/readme_images/validation_testing/terms-page.jpg)|Add html boilerplate, and moved header to become child to body tag|No error or warning. ![terms-page-fix](/static/images/readme_images/validation_testing/terms-page-fix.jpg)|
|Returns page|![returns-page](/static/images/readme_images/validation_testing/returns-page.jpg)|Add html boilerplate, and moved header to become child to body tag.|No error or warning. ![returns-page-fix](/static/images/readme_images/validation_testing/returns-page-fix.jpg)|

#### CSS Files [CSS W3C Jigsaw Validator](https://jigsaw.w3.org/css-validator/)
|Page Tested|Screenshot of Errors and Warnings   |Solution Applied|Screenshot of clear Validation Output|
|:------------|:----------------|:-------------|:------------|
|base.css|![base-css](/static/images/readme_images/validation_testing/base-css.jpg)|Add px as a unit to header-container class|![base-css-fix](/static/images/readme_images/validation_testing/base-css-fix.jpg)|
|blog.css|No error or warning. ![blog-css](/static/images/readme_images/validation_testing/blog-css.jpg)|N/A|![blog-css](/static/images/readme_images/validation_testing/blog-css.jpg)|
|checkout.css|No error or warning. ![checkout-css](/static/images/readme_images/validation_testing/checkout-css.jpg)|N/A|![checkout-css](/static/images/readme_images/validation_testing/checkout-css.jpg)|
|faq.css|No error or warning. ![faq-css](/static/images/readme_images/validation_testing/faq-css.jpg)|N/A|![faq-css](/static/images/readme_images/validation_testing/faq-css.jpg)|
|profile.css|No error or warning. ![profile-css](/static/images/readme_images/validation_testing/profile-css.jpg)|NA|![profile-css](/static/images/readme_images/validation_testing/profile-css.jpg)|
|terms.css|No error or warning. ![terms-css](/static/images/readme_images/validation_testing/terms-css.jpg)|N/A|![terms-css](/static/images/readme_images/validation_testing/terms-css.jpg)|

#### Python Files [PEP3 Validator](https://pep8ci.herokuapp.com/)
|Page Tested|Screenshot of Errors and Warnings   |Solution Applied|Screenshot of clear Validation Output|
|:------------|:----------------|:-------------|:------------|
|basket\views.py|No error or warning. ![basket-views](/static/images/readme_images/validation_testing/basket-views.jpg)|N/A|![basket-views](/static/images/readme_images/validation_testing/basket-views.jpg)|
|basket\contexts.py|No error or warning. ![basket-context](/static/images/readme_images/validation_testing/basket-context.jpg)|N/A|![basket-context](/static/images/readme_images/validation_testing/basket-context.jpg)|
|basket\urls.py|No error or warning. ![basket-urls](/static/images/readme_images/validation_testing/basket-urls.jpg)|N/A| ![basket-urls](/static/images/readme_images/validation_testing/basket-urls.jpg)|
|checkout\admin.py|No error or warning. ![checkout-admin](/static/images/readme_images/validation_testing/checkout-admin.jpg)|N/A|![checkout-admin](/static/images/readme_images/validation_testing/checkout-admin.jpg)|
|checkout\forms.py|No error or warning. ![checkout-form](/static/images/readme_images/validation_testing/checkout-form.jpg)|N/A|![checkout-form](/static/images/readme_images/validation_testing/checkout-form.jpg)|
|checkout\models.py|No error or warning. ![checkout-models](/static/images/readme_images/validation_testing/checkout-models.jpg)|N/A|![checkout-models](/static/images/readme_images/validation_testing/checkout-models.jpg)|
|checkout\signals.py|No error or warning. ![checkout-signals](/static/images/readme_images/validation_testing/checkout-signals.jpg)|N/A|![checkout-signals](/static/images/readme_images/validation_testing/checkout-signals.jpg)|
|checkout\urls.py|No error or warning. ![checkout-urls](/static/images/readme_images/validation_testing/checkout-urls.jpg)|N/A|![checkout-urls](/static/images/readme_images/validation_testing/checkout-urls.jpg)|
|checkout\views.py|No error or warning. ![checkout-views](/static/images/readme_images/validation_testing/checkout-views.jpg)|N/A|![checkout-views](/static/images/readme_images/validation_testing/checkout-views.jpg)|
|checkout\webhook_handler.py|No error or warning. ![checkout-webhook-handler](/static/images/readme_images/validation_testing/checkout-webhook-handler.jpg)|N/A|![checkout-webhook-handler](/static/images/readme_images/validation_testing/checkout-webhook-handler.jpg)|
|checkout\webhooks.py|No error or warning. ![checkout-webhook](/static/images/readme_images/validation_testing/checkout-webhook.jpg)|N/A|![checkout-webhook](/static/images/readme_images/validation_testing/checkout-webhook.jpg)|
|products\admin.py|No error or warning. ![product-admin](/static/images/readme_images/validation_testing/product-admin.jpg)|N/A|![product-admin](/static/images/readme_images/validation_testing/product-admin.jpg)|
|products\forms.py|No error or warning. ![product-form](/static/images/readme_images/validation_testing/product-form.jpg)|N/A|![product-form](/static/images/readme_images/validation_testing/product-form.jpg)|
|products\models.py|No error or warning. ![product-models](/static/images/readme_images/validation_testing/product-models.jpg)|N/A|![product-models](/static/images/readme_images/validation_testing/product-models.jpg)|
|products\urls.py|No error or warning. ![product-urls](/static/images/readme_images/validation_testing/product-urls.jpg)|N/A|![product-urls](/static/images/readme_images/validation_testing/product-urls.jpg)|
|products\views.py|No error or warning. ![product-views](/static/images/readme_images/validation_testing/product-views.jpg)|N/A|![product-views](/static/images/readme_images/validation_testing/product-views.jpg)|
|products\widgets.py|No error or warning. ![product-widget](/static/images/readme_images/validation_testing/product-widget.jpg)|N/A|![product-widget](/static/images/readme_images/validation_testing/product-widget.jpg)|
|profiles\forms.py|No error or warning. ![profile-form](/static/images/readme_images/validation_testing/profile-form.jpg)|N/A|![profile-form](/static/images/readme_images/validation_testing/profile-form.jpg)|
|profiles\models.py|No error or warning. ![profile-models](/static/images/readme_images/validation_testing/profile-models.jpg)|N/A|![profile-models](/static/images/readme_images/validation_testing/profile-models.jpg)|
|profiles\urls.py|No error or warning. ![profile-urls](/static/images/readme_images/validation_testing/profile-urls.jpg)|N/A|![profile-urls](/static/images/readme_images/validation_testing/profile-urls.jpg)|
|profiles\views.py|No error or warning. ![profile-views](/static/images/readme_images/validation_testing/profile-views.jpg)|N/A|![profile-views](/static/images/readme_images/validation_testing/profile-views.jpg)|

#### JavaScript Files [JavaScript Validator JSHint](https://jshint.com/)
|Page Tested|Screenshot of Errors and Warnings   |Solution Applied|Screenshot of clear Validation Output|
|:------------|:----------------|:-------------|:------------|
|quantity_script|No error. ![quantity-script](/static/images/readme_images/validation_testing/qauntity-script.jpg)|N/A|![quantity-script](/static/images/readme_images/validation_testing/qauntity-script.jpg)|
|stripe_elements.js|No error. ![stripe-elements](/static/images/readme_images/validation_testing/stripe-elelments.jpg)|N/A|![stripe-elements](/static/images/readme_images/validation_testing/stripe-elelments.jpg)|
|country_field.js|No error. ![country-fields](/static/images/readme_images/validation_testing/country-fields.jpg)|N/A|![country-fields](/static/images/readme_images/validation_testing/country-fields.jpg)|

### Browser compatibility
|Browser Tested|Functionality Tested|Visual Consistency|Outcome|
|:------------:|:----------------:|:-------------:|:-------------:|
|![chrome](/static/images/readme_images/browser-compatibility-test/chrome.jpg)|Navigations, Forms, Links and Buttons|Layout, design, content display consistency|Intended appearance and responsiveness is good|
|![edge](/static/images/readme_images/browser-compatibility-test/edge.jpg)|Navigations, Forms, Links and Buttons|Layout, design, content display consistency|Intended appearance and responsiveness is good|
|![firefox](/static/images/readme_images/browser-compatibility-test/firefox.jpg)|Navigations, Forms, Links and Buttons|Layout, design, content display consistency|Intended appearance and responsiveness is good|
### Screen sizes Responsiveness
|Device Tested|Site responsive >=700px |Site responsive <699px|Render as expected|
|:------------:|:----------------:|:-------------:|:--------------:|
|iPhone 12 Pro (Mobile)|N/A|Good|Good 390px X 844px ![iPhone-12-pro](/static/images/readme_images/screen-size-responsivness-test/iphone-12%20pro.jpg)|
|iPad Mini (Tablet)|Good|N/A|Good 768px X 1024px ![ipad-mini](/static/images/readme_images/screen-size-responsivness-test/ipad-mini.jpg)|
|iPad Air (Laptop)|Good|N/A|Good 820px X 1180px ![ipad-air](/static/images/readme_images/screen-size-responsivness-test/ipad-air.jpg)|
|Nest Hub Max (Desktop)|Good|N/A|Good 1280px X 800px ![nest-hub-max](/static/images/readme_images/screen-size-responsivness-test/nest-hub-max.jpg)|

### Pages Responsivnes
|Home Page|Products Page|Product Detail Page|Basket Page|Checkout Page|Product Management Page|
|:------------:|:----------------:|:-------------:|:--------------:|:--------:|:------:|
|![home-page](/static/images/readme_images/page-responsivness/home-page.jpg)|![products-page](/static/images/readme_images/page-responsivness/products-page.jpg)|![product-detail-page](/static/images/readme_images/page-responsivness/products-details.jpg)|![basket-page](/static/images/readme_images/page-responsivness/basket-page.jpg)|![checkout-page](/static/images/readme_images/page-responsivness/checkout-page.jpg)|![product-management-page](/static/images/readme_images/page-responsivness/product-management-page.jpg)|
## Technologies Used
* Bootstrap
* Django
* Amazon Web Service
* Database
* Heroku
* Stripe
### Languages Used
* Python
* JavaScript
* HTML
* CSS
* DTL
## Bugs
#### Bugs Resolved
|Bug|   Description |Solution Applied|Result|
|:------------|:----------------|:-------------|:------------|
|Basket, search and account duplication|After created mobile-top-header.html, on rendering when I try to reduce the size of screen the account, basket and search tends to duplicate when screen is reduced from 992px. ![duplicate](/static/images/readme_images/bugs/duplicate.jpg)|Added “d-lg-none" class to account basket and search|Bug fixed. ![duplicate-fix](/static/images/readme_images/bugs/duplicate-fix.jpg)|
|Webhook Handler|After making a purchase it shows successful on frontend, however there is internal server error 500 on /check/wh printed on python terminal. On stripe CLI it also shows 500 POST error. However stripe portal shows that payment intent is created and charge succeeds. ![webhook-handler1](/static/images/readme_images/bugs/webhook-handler1.jpg) ![webhook-handler2](/static/images/readme_images/bugs/webhook-handler2.jpg) ![payment-intent](/static/images/readme_images/bugs/payment-intent.jpg) ![log](/static/images/readme_images/bugs/log.jpg)|Followed below steps **1**. Get the payment intent from Stripe. **2**. Get the basket metadata. **3**. Get the billing and shipping details. **4**. Attempt to get the order object (if it exists), trying 5 times. **5**. If the order exists, verify the order in the database. **6**. If it doesn't exist (else), create the order in the database. **7**. When creating the order, included an exception catch to throw and 500 your Devtools > Network tab.|Bug fixed. ![webhook-handler-fix](/static/images/readme_images/bugs/webhook-handler-fix.jpg)|
|Checkout form|When checkout form is not properly completed and “complete order” is clicked, form throws up a toast error message which is expected, however the payment_entent.succeed goes through in stripe and confirmation email sent to user.|Added fields validation for checkout form, hence form does not submit unless all fields are validated. Therefore payment_intent.succeeded and confirmation email can only go through when form is properly completed. ![form-validation](/static/images/readme_images/bugs/form-field.jpg)|Bug fixed. Only payment_intent.created is ready at this time until form is properly completed before payment_intent.succeeded can go through|

## Libraries
* Django-allauth
* Django-countries
* django-crispy-forms
* Django-phonenumber
* Pillow
* Psycopg2==2.9.10
* Setup tools
* Gunicorn
* Boto
## Deployment
### Local Deployment
|Steps|  Action |
|:------------|:----------------|
|PostgreSQL Database|Navigate to [PostgreSQL from Code Institute] (https://dbs.ci-dbs.net) and ender your email and submit. Database link will be sent to your email|
|Create a new Heroku app|Click new to crate a new app. [new-app](/static/images/readme_images/Deployment/new-app.jpg) [new-app2](/static/images/readme_images/Deployment/new-app2.jpg) Go to settings and open Config Vars and add config var DATABASE_URL, then copy PostgreSQL sent to your email. [settings](/static/images/readme_images/Deployment/settings.jpg) [database-url](/static/images/readme_images/Deployment/database%20url.jpg)|
|Connect  DB to local development web server|Install dj_database_url using pip command and update requirements.txt. In settings.py import dj_database_url [import-dj](/static/images/readme_images/Deployment/import-dj.jpg). In settings.py in DATABASE section add below code [database](/static/images/readme_images/Deployment/database.jpg) In the teminal run showmigration command to ensure you are connected to external database. Migrate database models to new database. Then load data starting with categories then products. Crease a new super user. Before pushing to GitHub delete external database from setting.py|
### Heroku Deployment
|Steps|  Action |
|:------------|:----------------|
|Hide SECRET_KEY|Generate a secret key and add to env.py using below code [secret-key](/static/images/readme_images/Deployment/secret-key.jpg). Update secret key in setting.py [secret-key2](/static/images/readme_images/Deployment/secret-key2.jpg). Import os to env.py. Import env at the top of settings.py|
|Ready project for deplyment|Update database session in setting.py to ensure development environment continues uding  local SQLite DB and can access external DB [update-code](/static/images/readme_images/Deployment/update-code.jpg). Import env model into settings and update the code to check if the file exist in the environment before importing since env.py is not commited to GitHb hence Heroku cannot acces it. [import-env](/static/images/readme_images/Deployment/import-env.jpg). Then create a Procfile [procfile](/static/images/readme_images/Deployment/procfile.jpg). Inside Procfile add code to instruct Heroku to create web dyno and run guncorn to serve Eco shop app [procfile2](/static/images/readme_images/Deployment/procfile2.jpg). Add runtime.txt to root directory and include python version [runtime](/static/images/readme_images/Deployment/runtime.jpg). Return to Heroku and open the app you created and copy the link [heroku-eco](/static/images/readme_images/Deployment/heroku-eco.jpg). Add ULR to ALLOWED_HOSTS in setting.py, ensure https:// is removed [allowed-host](/static/images/readme_images/Deployment/allowed-host.jpg)|
|Install gunicorn| Use pip install gunicorn command to install and update|requirments.txt. Save and push changes to GitHub.
|Ready Heroku settings for deplyment|In Heroku navigate to app settings and open Config Vars. Create environment varaible DISABLE_COLLECTSTATIC and give it value of 1 [collectstatic](/static/images/readme_images/Deployment/collectstatic.jpg). Create a new varaible SECRET_KEY and set value to random key you must have generated [heroku-secret-key](/static/images/readme_images/Deployment/heroku-secret-key.jpg)|
|Deploying Eco Shop App|Select Deploy on Heroku dashboard [deploy](/static/images/readme_images/Deployment/deploy.jpg). Ensure Heroku App is linked to GitHub repository [connection](/static/images/readme_images/Deployment/connection.jpg). Deploy barch to project [branch](/static/images/readme_images/Deployment/branch.jpg). Watch the build and view activity tab on dashboard. After build click open app button to view the project|
|Setting DEBUG|In settings.py set DEBUG to True only if environment variable called DEVELOPMENT is present [debug](/static/images/readme_images/Deployment/debug.jpg). Add new varaible in env.py DEVELOPMENT and set to 1 and push to GitHub[dev1](/static/images/readme_images/Deployment/dev1.jpg)|

## Credits
### Codes
* Code Institue eCommerce Project. **Boutique Ado**
### Tutorials
* Tutor Support
* [stackoverflow](https://stackoverflow.com/questions)
### Photos
* Product images and description : [Peace with the wild](https://www.peacewiththewild.co.uk/)















