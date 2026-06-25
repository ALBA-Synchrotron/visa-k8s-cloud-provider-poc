Feature: MyObjectName CRUD Testing

  Scenario: Do a preventive logout
    Given I am on CAS logout page

  Scenario: Do the logout and login on CAS page
    Given I am on CAS login page
    When I enter "mistest" in the "username" text field
    And I enter "12345" in the "password" text field
    And I click on the CAS submit button
    Then I should be redirected to CAS Login Page


#### CREATE ####
  Scenario: Access to the new MyObjectName Form
    Given I am on the "my_object_name/new/" page
    And I wait "1" seconds for the page to be loaded
    Then  I should see the element with id "generic_form_submit_btn"
    And  I should see the element with id "id_back_button"


#### READ list ####
  Scenario: Access to the MyObjectName list
    Given I am on the "my_object_name/" page
    And I wait "1" seconds for the page to be loaded
    Then  I should see the element with id "my_object_name_list"


#### READ detail ####
  Scenario: Access to MyObjectName detail
    Given I am on the "my_object_name/1" page
    And I wait "1" seconds for the page to be loaded
    Then  I should see the element with id "id_title_detail"
    And  I should see the element with id "id_back_button"


#### UPDATE ####
  Scenario: Enter MyObjectName update page and check elements
    Given I am on the "my_object_name/1/update" page
    And I wait "1" seconds for the page to be loaded
    Then I should see the element with id "id_back_button"
    And  I should see the element with id "generic_form_submit_btn"


#### DELETE ####
  Scenario: Enter MyObjectName delete page and check elements
    Given I am on the "my_object_name/1/delete" page
    And I wait "1" seconds for the page to be loaded
    Then I should see the element with id "id_back_button"
    And  I should see the element with id "generic_form_confirm_delete_btn"


