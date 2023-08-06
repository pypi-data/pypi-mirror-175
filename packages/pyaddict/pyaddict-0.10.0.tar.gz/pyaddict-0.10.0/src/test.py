from pyaddict import JDict, JList

jdict = JDict({
    "name": "John",
    "age": 30,
    "cars": [
        {"model": "BMW 230", "mpg": 27.5},
        {"model": "Ford Edge", "mpg": 24.1}
    ]
})

# jdict
print(jdict.ensureCast("name", str))  # John
print(jdict.ensureCast("age", int))  # 30
print(jdict.ensureCast("age", str))  # "30"
print(jdict.optionalGet("age", str)) # None
print(jdict.optionalCast("age", str))  # "30"
print(jdict.optionalGet("gender", str)) # None
print(jdict.optionalCast("gender", str)) # None
print(jdict.ensure("gender", str)) # ""

# jlist
cars = jdict.ensureCast("cars", JList)
print(cars.ensureCast(0, JDict).ensureCast("mpg", str))  # "27.5"
print(cars.ensureCast(1, JDict).ensureCast("mpg", str))  # "24.1"
print(cars.ensureCast(2, JDict).ensureCast("mpg", str))  # ""
print(cars.ensureCast(2, JDict).optionalGet("mpg", str))  # None
# print(cars.assertGet(2, JDict))  # AssertionError

# chaining
print(jdict.chain().resolve("cars.[0].model")) # "BMW 230"
#print(jdict.chain().resolve("car.[0].model")) # KeyError

print(jdict.chain().ensureCast("car.[0].model", str)) # ""
print(jdict.chain().optionalGet("car.[0]?.model", str)) # None
print(jdict.chain().optionalCast("car.[0]?.model", str)) # None

x = jdict.chain()["cars.[1].model"]
