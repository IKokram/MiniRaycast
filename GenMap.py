from random import randint, choice

def generate(w_size, h_size, density=7, step=100000):
	WIDTH = w_size
	HEIGHT = h_size

	mas = [["#"] * WIDTH for _ in range(HEIGHT)]

	density = density
	px, py = randint(1, WIDTH-2), randint(1, HEIGHT-2)
	spx, spy = px, py
	poses = [[px, py]]
	mas[py][px] = " "

	step = step

	while poses and step > 0:
		directs = [[1, 0], [0, -1], [-1, 0], [0, 1]]
		dx, dy = px, py

		while directs:
			vector = directs.pop(randint(0, len(directs)-1))
			px, py = px + vector[0], py + vector[1]
			if ((0 < px < WIDTH-1) and (0 < py < HEIGHT-1)) and mas[py+vector[1]][px+vector[0]] != " " and mas[py][px] != " ":
				fa = 0
				for dpx in range(-1, 2):
					for dpy in range(-1, 2):
						if mas[py+dpy][px+dpx] != " ":
							fa += 1
				if fa >= density:
					break
				else:
					px, py = px - vector[0], py - vector[1]
			else:
				if mas[py][px] == "#": mas[py][px] = "$"
				px, py = px - vector[0], py - vector[1]

		if dx == px and dy == py:
			px, py = poses.pop()
		else:
			poses.append([px, py])
			step -= 1
		mas[py][px] = " "

	r = ""
	for line in mas:
		r += "".join(line) + "\n"
	r = r[:-1]

	return spx, spy, r


