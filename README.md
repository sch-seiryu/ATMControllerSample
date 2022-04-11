# ATM Controller Sample
An implementation of a simple ATM controller with its test codes, as a custom task sample project.

## 1. Instructions
* You can clone project from this GitHub repository as you wish.
* Project language is Python 3+ 
* <i>'atm_controller.py'</i> has all of the features requested, but have no specific entry point.
    * <i>'driver.py'</i> has an entry point like a driver class, and this is a presumed way to start the integrated system.
* <i>'test/test_atm_controller.py'</i> is a test code based on Python <i>'unittest'</i> module. You can run a test with this file.(also has entry point)

## 2. Documentary
### 2.1 Requirements & Prerequisites
* There are four stages given, and corresponding actions are required for each stage. <p style="text-align: center; ">
<b>Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw</b></p>
* Only dollars are counted; data type for money/balance will be an integer type.
* It is unnecessary to implement or to try integration with real ATM machine(hardware) and core banking system parts;
but keep in mind that the jobs would be done in the future. 
* There's a 'bank API' provided to examine that the PIN number is correct.
* It is allowed to simplify some complex problems, and the development of core structure of ATM software and corresponding tests are main goal of this project.   

### 2.2 Insights & Approaches
* First of all, requirements seemed to be simple. The work flow is quite straight forward, so it would be easy to describe it into finite states.
* The controller has a 'Session', which is a kind of lifecycle for each use case.
* Concerning single thread program. The controller basically has the context(main-thread), and call hardware input if necessary.(blocking operation)
* For integrity of the controller, both 'bank API' and 'hardware driver' are referenced by the controller, not vice versa.
    * This may disable both hardware and software interruptions in real world situations; but let's keep it simple.

### 2.3 Troubles & Concerns
* How can I get accounts when PIN number is correct? -> Assuming that there's an another bank API that I can retrieve those accounts.
* It would be better with async control in real example, but for simplification and easy testing, the technique is renounced.
