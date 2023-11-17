# Insurance Quote App
This is a Django application providing an API for managing insurance quotes. The entire problem statement is at the end 

https://sure.notion.site/2022-Backend-Take-Home-Prompt-5fd6c44daa55421081b144778e07ff68
...

## Getting Started

### Prerequisites
Python 3.12.0 is recommended. 
> Optional: 
If `asdf` is already installed then running `asdf install` shall install python 3.12.0 based on `.tool-versions`. However, this is not required but if still interested then refer to the [asdf documentation](https://asdf-vm.com/#/core-manage-asdf) for installation instructions 

This app uses Poetry for the virtual environment and dependency management.


1. **Install Poetry:**

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    Or refer to the [official Poetry installation guide](https://python-poetry.org/docs/#installation) for other methods.
<br>

2. **Install Dependencies:**
    Inside this project folder, run the following

    ```bash
    poetry install
    ```

3. **Run Migrations:**

    ```bash
    poetry run python manage.py migrate
    ```

5. **Create Superuser:**

    ```bash
    poetry run python manage.py createsuperuser
    ```

6. **Run the Development Server:**

    ```bash
    poetry run python manage.py runserver
    ```

7. **Access the App:**

    Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) It automatically redirects you to the Admin page.
<br>


## Usage
The three states are already populated with the configuration
![image info](./images/state_configs.png)
![image info](./images/state_config.png)

### Submit Quote
```curl
 curl -X POST http://localhost:8000/insurance/quote/ -H "Content-Type: application/json" -d '{"buyer_name": "John Doe", "coverage_type": "Basic", "state": "California", "has_pet": true, "coverage": {"flood":true}}' 
 ```
 ![image info](./images/quote.png)
### Get Quote
```
curl -X GET http://localhost:8000/insurance/quote/1/
```
This Returns the following
```JSON
{
  "id": 5,
  "buyer_name": "John Doe",
  "coverage_type": "Basic",
  "state": "California",
  "has_pet": true,
  "coverage": {
    "flood": true
  },
  "pricing": {
    "Monthly Subtotal": 40.8,
    "Monthly Taxes": 0.4,
    "Monthly Total": 41.2
  }
}
```

## Testing

**Run Unit Tests:**

```bash
poetry run python manage.py test
```

---
<br>
<br>
<br>
<br>


# Problem Statement:
https://web.archive.org/web/20231117083958/https://sure.notion.site/2022-Backend-Take-Home-Prompt-5fd6c44daa55421081b144778e07ff68

# 2022 Backend Take Home Prompt
# Challenge

Acme Home Insurance is building out an insurance product, and needs you to implement their pricing algorithm. Your solution should include the following:

- Implement a Quote structure that is persisted for later retrieval. The Quote should store data necessary to determine pricing and should have an ID or similar mechanism to retrieve the Quote’s data.
- Implement a feature where given the ID of a Quote, the pricing is assessed and returned. See “Cost Calculations” below for more details.
- A README should be included with your project with relevant details for setup, test, and running your application.

## **Technical Requirements:**

Below are technical requirements that should help when assessing how your solution should be implemented.

- We suggest Python 3 or later.
- You may use any application frameworks or tools you’d like, though are not required to do so. If you choose to make use of specific tools, make sure to include any setup and usage instructions within your README that may be needed.
- How you persist Quotes is up to you as long as they can be **stored** and **retrieved** for later usage i.e. pricing.
- Your solution should be appropriately unit tested and include any details on how to run automated tests.

## Quote Object:

A quote object is the object that tells us what the user is wanting to purchase insurance for, and what kind of coverage they are selecting.  Quotes must be persisted so that they can be viewed later.

For Acme Homeowners Insurance, a quote will contain the following fields:

- The buyer’s name
- Coverage type - they can choose “Basic” or “Premium”
- The state of the buyer - California, New York, or Texas
- Does the buyer have a pet?
- Does the buyer want flood coverage?

## Cost Calculations:

The base cost is derived from the plan that the user is purchasing.

- If the user is getting basic coverage, charge $20/month.
- If the user is getting premium coverage, charge $40/month.

Then we add the pet coverage premium:

- If the user has a pet, add $20/month to the cost.
- Otherwise, keep the cost as is.

For the first iteration of Acme homeowners insurance, we will support three different states.  These states each have their own flood coverage rate and monthly tax rate.

### California:

- If the user is buying flood coverage, increase cost by 2%
- Monthly Tax: 1%

### Texas:

- If the user is buying flood coverage, increase cost by 50%
- Monthly Tax: .5%

### New York:

- If the user is buying flood coverage, increase cost by 10%
- Monthly Tax: 2%

## The Pricing Algorithm:

The rater function will be passed a quote ID which can be used to look up a quote from the database.

The output of the rater function needs to include the following:

- The monthly price without taxes for the quote (Subtotal).
- The monthly taxes for a quote.
- The total monthly price for a quote.

When designing the price calculator, use the following considerations to guide your implementation:

- We want to design this in a way that it will be easy to add more states. Eventually we want to add all 50 states, and want to make it easy to do so in the future.
- The pricing algorithm should be designed in a way to allows new variables to be easily added. For example, it should be easy to add in hurricane coverage.
- The individual variables for the pricing algorithm should be easy to modify, ideally without changing or deploying new code. For example, updating flood coverage in New York from 10% to 20% should be a simple task.

## Acceptance Test Cases

You can use these example Quote pricing acceptance test cases to help validate the correct pricing algorithm. NOTE: this is not an exhaustive test suite and you should choose how best to test your solution.

**Quote 1:**

Coverage Type: Basic

State: California

Has Pet: True

Flood Coverage: True

Price:

Monthly Subtotal: $40.80

Monthly Taxes: $0.40

Monthly Total: $41.20

**Quote 2:**

Coverage Type: Premium

State: California

Has Pet: True

Flood Coverage: True

Price:

Monthly Subtotal: $61.20

Monthly Taxes: $0.61

Monthly Total: $61.81

**Quote 3:**

Coverage Type: Premium

State: New York

Has Pet: True

Flood Coverage: False

Price:

Monthly Subtotal: $60

Monthly Taxes: $1.20

Monthly Total: $61.20

**Quote 4:**

Coverage Type: Basic

State: Texas

Has Pet: False

Flood Coverage: True

Price:

Monthly Subtotal: $30

Monthly Taxes: $0.15

Monthly Total: $30.15
