# ebay-category-id-mapper
This is a short python class to map ebay categories Ids from Ebay categories names

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* This bot has been built on Ubuntu 18.04 using Python 3.7.5 and it has not been tested on other OSS. 
* Dependencies used are listed in the requirements.txt file.  
* Data used is obtained from Ebay and sligthly modified for performance, memory and readability

### Installing

1. Clone the repository
```
git clone https://github.com/federiva/ebay-category-id-mapper
```
3. Recommended: Create a virtual [environment](https://docs.python.org/3/library/venv.html)

4. Install dependencies from requirements.txt to your virtual environment or directly into your global environment.
```
 pip install -r requirements.txt 
```
5. Use or embed it into your application

## Examples

```
category_example = 'Beauty & Gesundheit >> Make-up >> Augen >> Lidschattenstifte'
mapper = categoryMapper()
id_category_in = mapper.map_category_to_id(category_example)
print(id_category_in)
```
Which returns 172022 that you can check at:  
https://www.ebay.de/b/172022

## Authors

* **Federico Rivadeneira** - *Initial work* - [federiva](https://github.com/federiva)

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details
