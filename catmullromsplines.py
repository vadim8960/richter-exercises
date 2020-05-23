from math import *
import numpy as np

def calc_len(p1, p2):
	return sqrt(((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])))

def make_single_spline(p1, p2, p3, p4, count, tao):
	p_x = np.matrix([[p1[0]],[p2[0]],[p3[0]],[p4[0]]])
	p_y = np.matrix([[p1[1]],[p2[1]],[p3[1]],[p4[1]]])
	res = []
	t = 0

	m_mat = np.matrix([
						[   0   ,     1  ,     0      ,  0   ],
						[  -tao ,     0  ,    tao     ,  0   ],
						[2 * tao, tao - 3, 3 - 2 * tao, -tao ],
						[ -tao  , 2 - tao,   tao - 2  ,  tao ]
					  ])

	while (t <= 1):
		t_mat = np.matrix([1, t, (t**2), (t**3)])
		r = t_mat * m_mat
		x = r * p_x
		y = r * p_y
		t += (1 / count)
		res.append((x.item(), y.item()))
	return res

def catmullrom_splines(points):
	res = []
	p_begin = points[0]
	p_end = points[len(points) - 1]

	delta_b = (p_begin[0] - points[1][0], p_begin[1] - points[1][1])
	delta_e = (points[len(points) - 2][0] - p_end[0], points[len(points) - 1][1] - p_end[1])

	p_begin = (p_begin[0] - delta_b[0] / calc_len(p_begin, delta_b), p_begin[1] - delta_b[1] / calc_len(p_begin, delta_b))
	p_end = (p_end[0] + delta_e[0] / calc_len(p_end, delta_e), p_end[1] + delta_e[1] / calc_len(p_end, delta_e))

	points.insert(0, p_begin)
	points.append(p_end)

	tao = 0.75

	res.extend(make_single_spline(points[0], points[1], points[2], points[3], 100, tao))

	for i in range(1, len(points) - 4):
		c = make_single_spline(points[i], points[i + 1], points[i + 2], points[i + 3], 100, tao)
		res.extend(c)

	res.extend(make_single_spline(points[len(points) - 4], points[len(points) - 3], 
								  points[len(points) - 2], points[len(points) - 1], 100, tao))

	points.remove(p_begin)
	points.remove(p_end)
	return res
