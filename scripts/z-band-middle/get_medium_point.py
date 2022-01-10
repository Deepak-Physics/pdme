import random
import logging

def get_uniform_sphere():
	r = random.random()**.3333 * 10
	a = random.uniform(-10, 10)
	b = random.uniform(-10, 10)
	c = random.uniform(-10, 10)
	f = (a**2 + b**2 + c**2)**.5
	return (a * r / f, b * r / f, c * r / f)


def get_pt():
	return (get_uniform_sphere(), (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(3.5, 4.5)))

def main():
	logging.info(get_pt())

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	main()
