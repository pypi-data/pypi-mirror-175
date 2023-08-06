from pyaddict import JDict, JList

jdict = JDict({
    "name": "John",
    "age": 30,
    "cars": [
        {"model": "BMW 230", "mpg": 27.5},
        {"model": "Ford Edge", "mpg": 24.1}
    ]
})

# Get value
print(jdict.ensure("name", str))  # John
print(jdict.ensure("age", int))  # 30
print(jdict.ensure("age", str))  # ""
print(jdict.ensureCast("age", str))  # "30"
print(jdict.optionalGet("age", str)) # None
print(jdict.optionalCast("age", str))  # "30"
print(jdict.optionalGet("gender", str)) # None
print(jdict.optionalCast("gender", str)) # None
print(jdict.ensure("gender", str)) # ""

cars = jdict.ensureCast("cars", JList)
print(cars.assertGet(1, dict))  # {'model': 'Ford Edge', 'mpg': 24.1}
print(cars.assertGet(2, dict))  # AssertionError

# iterators
for car in cars.iterator().ensureCast(JDict):
    print(car.ensureCast("model", str)) # BMW 230, Ford Edge

# chaining
chain = jdict.chain()
print(chain.ensureCast("cars.[1].mpg", str))  # "24.1"
print(chain.ensureCast("cars.[2].mpg", str))  # ""
# or via direct access (returns Optional[Any]!)
print(chain["cars.[2].mpg"])  # IndexError
print(chain["cars.[2]?.mpg"])  # None
