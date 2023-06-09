# Usage

## Report

> **Note**
>
> CMMS provides 3 types of report,
> * Installation
> * Daily inspection
> * PPM

### Installation Report

For all the equipment there is an installation report that shows when a device arrived, installed, warranty period, purchase cost, and PM schedule.

There are some steps you must do to get your installation report:

1. Press on "*ADD EQUIPMENT*"

   ![1](images/add_equipment_installation.jpeg)

2. Fill up the form

   ![2](images/form.png)

3. After filling it in, an Equipment Card will appear with all equipment information. Press here "(...)" to get your Installation Report

   ![3.1](images/the_new_equipment.jpeg)

   ![3.2](images/installation_report.jpeg)

### Daily Inspection Report

Daily inspection Report is filled by an Engineer to ensure the safety of the device and its accessories in each department and check if the device needs maintenance or not.

There are some steps to fill this report:

1. Sign in as a Clinical Engineer

   ![1](images/sign_in.jpeg)

2. Fill in the report then click **Save**

   ![2](images/daily_inspection.jpeg)

To see your saved report:

1. Press log out

  ![1](images/logout.jpeg)

2. Sign in as an Admin

  ![2](images/sign_in_daily_inspec.jpeg)

3. On the sidebar, find and click **Reports** > **Daily Inspection**

  ![3](images/home_reports.png)

4. On the saved report list, click "(...)" to see the report's details

  ![4](images/final_daily_inspec.jpeg)

5. After that, you'll see the final form for Daily Inspection Report of a device (in this example it's **Steam Sterilizer**)

  ![5](images/daily_inspec.jpeg)

### PPM (Planned Preventative Maintenance) Report

For all Equipment, there is a PPM report that is filled with a specific schedule to make sure that the device/accessories need to be maintained or that it is working effectively.

There are some steps to fill in this report:

1. Sign in as a clinical engineer

   ![1](images/sign_in.jpeg)

2. All reports will appear, on the sidebar, choose **Red** PPM. A small Form will appear choose the Equipment, fill it in and then click on **Blue** PPM

   ![2](images/PPM1.png)

3. Here is PPM report for C-Arm 680 OR device, Fill it in then click **Save**

   ![3](images/PPM2.png)

To see your saved report:

1. Press log out

   ![1](images/logout.jpeg)

2. Sign in as an Admin

   ![2](images/sign_in_daily_inspec.jpeg)

3. On the sidebar, find and click **Reports** > **PPM**

   ![3](images/PPM3.png)

4. On the saved report list, click "(...)" to see the report's details

   ![4](images/PPM4.png)

5. After that, you'll see the final form for PPM Report of a device (in this example it's **C-Arm 680 OR**)

   ![5](images/PPM5.png)

## Departments

> **Note**
>
> We have 4 departments: **OR**, **ICU**, **Radiology**, **CSSD**.  
> Each department has its own information, such as:
> * The Code of the department
> * The Location of the department
> * The Equipment's number
> * The Engineers' number working in it.

![1](images/1.png)


To add a new department:

1. Click (*ADD DEPARTMENT*) button

![1](images/2.png)

2. Fill the form, then click **Add**

![2](images/Dept_Add_Form.png)

You can get detailed information for each Department by clicking the "(...)" button,

![1](images/3.png)

A table will appear that shows information about all the Equipment included in a certain Department. These information as shown are the Equipment's:
* Code
* Name
* Cost
* Model
* Serial Number

![1](images/Dept_Equip.png)

There is another page "Clinical Engineers". This page shows all the Clinical Engineers who are mainly responsible for certain Department.

![1](images/Dept_more_CE.png)

## The Equipment
> **Note**
>
> This includes all equipment of each Department.
> Each Equipment has its own information such as the Equipment's:
> * Name
> * Code
> * Model
> * Serial number
> * Location
> * Department

![1](images/4.png)

You can add a new equipment:

1. Click **ADD EQUIPMENT** button

![1](images/5.png)

2. Fill the form, then click **ADD**

![2](images/Equip_Add_Form.jpeg)

You can edit or delete Equipment by clicking one of these buttons:

![1](images/6.png)

Here is the Edit form of an equipment:

![1](images/Eq-edit.jpeg)

To see more information about each equipment, Click the "(...)" button

![1](images/more_option_equipment.png)

From here you can view the Equipment's Reports:

![1](images/Equip_more_Reports.png)

When choosing Installation, the installation report of the Equipment will appear:

![1](images/install.png)

When choosing PPM, the PPM report of the Equipment will appear:

![1](images/Equipment_more_PPM.png)

When choosing Daily Inspection, the Daily Inspection of the Equipment will appear:

![1](images/Equip_more_Daily.png)

From here you can view the Equipment's Spare Parts, Breakdowns, and Maintenance:

![1](images/more_info2_equipment.png)

When choosing **Spare Parts**:

![1](images/spare_parts.png)

When choosing **Break downs**:

![1](images/break_downs.png)

When choosing **Maintenance** :

![1](images/maintenance2.png)


## Work Orders

Managing work orders is one of the important features in CMMS systems. So, we added this feature to our project.

### Admin

* View all the work orders
   * The Code of the order
   * The Start and End date
   * The Description
   * The Engineer associated with the order
   * The Equipment associated with the order
   * The Cost
   * The Priority of the order marked with colors

![Work Orders](images/workorder.png)

* Add new orders

![Add work order](images/addworkorder.png)

* Edit any specific work order

![Edit work order](images/editworkorder.png)

* Delete any specific work order

### Clinical Engineer

After log in the clinical engineer can view all his work orders in a calendar, the color represents the priority of the order.

![chalender](images/chalender1.png)

![chalender list](images/chalender2.png)

## Breakdowns

Recording all the breakdowns that happened in your system is very important for decision making and statistics. So, in our project the admin can view all the break downs in detail.

### Admin
* View all the break downs
   * The Code of the breakdown
   * The Reason of the breakdown
   * The Equipment which is broken down
   * The Date
   * The Department of the equipment

![Break Downs](images/breakdown.png)

* Add new breakdowns

![Add break down](images/addbreakdown.png)

* Edit any specific breakdown

![Edit break down](images/editbreakdown.png)

* Delete any specific breakdown

## Maintenance

Recording all the maintenance operations in your system is very important for decision making and statistics. So, in our project the admin can view all the maintenance operations in detail.

### Admin
* View all the maintenance operations
   * The Code of the maintenance
   * The Start and End Date
   * The Description of the maintenance
   * The Equipment associated with the maintenance operation
   * The Engineer who made the maintenance operation
   * The Department
   * The breakdown associated with this maintenance

![Maintenence](images/maintenance.png)

* Add new maintenance

![Add maintenance](images/addmaintenance.png)

* Edit any specific maintenance

![Edit maintenance](images/editmaintenance.png)

* Delete any specific maintenance

## Spare Parts

* The card of each Spare Part include some information such as the Spare Part's:

  * Code
  * Name
  * Amount
  * Equipment Code
  * Agent ID

![2](images/Spare_Info.png)

* Here we can **Add** any new Spare part entering the Database :

![1](images/Spare_Add_btn.png)

* When adding a new Spare Part, this form should be filled in first:

![2](images/Spare_Add_Form.png)

* From here you can edit or delete any Spare Part:

![2](images/Spare_Edit_btn.png)

* When editing any Spare Part a form like this will appear:

![2](images/Spare_Edit.png)

## Agent / Suppliers

* The table is showing information about each agent such as the agent's:
  * ID
  * Name
  * Address
  * Phone Number
  * E-mail or Fax

![2](images/Agent_Info.png)

* Here we can **Add** any new agent or supplier we are dealing with :

![2](images/Agent_Add_btn.png)

* And this will be done by filling in this form:

![2](images/Agent_Add_Form.png)

* We can edit or delete any information about our agents from here:

![2](images/Agent_Edit_btn.png)

* The Edit form will appear as the following one:

![2](images/Agent_Edit.png)

* To know more about the dealing with each agent, we can click on the more (...) button:

![1](images/Agent_extra_btn.png)

* This will show a table including any Spare Parts we have from this agent:

* The Code of each Spare Part and its amount are shown too.

![1](images/Agent_more_Spare.png)

* When choosing Equipment, a table will appear including all the Equipment data that we own from each Agent or Supplier:

![1](images/Agent_more_Equip.png)
