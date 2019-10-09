import numpy as np

def make_derivative(p1, p2):
	# return (p1[0], (p1[1] - p2[1]) / (p1[0] - p2[0]))
	return (p1[0], (p1[1] - p2[1]) / 2)

def make_single_spline(p1, p2, p3, p4, count, pp):
	p_x = np.matrix([[p1[0]],[p2[0]],[p3[0]],[p4[0]]])
	p_y = np.matrix([[p1[1]],[p2[1]],[p3[1]],[p4[1]]])
	res = []
	t = 0
	tao = 0.5

	# m_mat = np.matrix([[0, 2, 0, 0], [-1, 0, 1, 0], [2, -5, 4, -1], [-1, 3, -3, 1]])

	m_mat = np.matrix([[1, 0, 0, 0], [0, 0, 1, 0], [-3, 3, -2, -1], [2, -2, 1, 1]])

	# m_mat = np.matrix([
	# 					[   0   ,     1  ,     0      ,  0   ],
	# 					[  -tao ,     0  ,    tao     ,  0   ],
	# 					[2 * tao, tao - 3, 3 - 2 * tao, -tao ],
	# 					[ -tao  , 2 - tao,   tao - 2  ,  tao ]
	# 				  ])

	if pp == 0:
		m_mat = m_mat * np.matrix([[0, 1, 0, 0],[0, 0, 1, 0], [1, 0, 0, 0], [0, -1/2, 0, 1/2]])
		p_x[0] = 0
	elif pp == 1:
		m_mat = m_mat * np.matrix([[0, 1, 0, 0],[0, 0, 1, 0], [-1/2, 0, 1/2, 0], [0, -1/2, 0, 1/2]])
	elif pp == 2:
		m_mat = m_mat * np.matrix([[0, 1, 0, 0],[0, 0, 1, 0], [0, -1/2, 0, 1/2], [0, 0, 0, 1]])
		p_x[3] = -100

	while (t <= 1):
		# t_mat = np.matrix([1, t, (t**2), (t**3)])
		# t_mat = np.matrix([1/2, (t**1)/2, (t**2)/2, (t**3)/2])
		t_mat = np.matrix([1, (t**1), (t**2), (t**3)])
		r = t_mat * m_mat
		x = r * p_x
		y = r * p_y
		t += (1/count)
		res.append((x.item(), y.item()))
	return res

def catmullrom_splines(points):
	res = []
	p_begin = make_derivative(points[0], points[2])
	p_end = make_derivative(points[len(points) - 3], points[len(points) - 1])

	points.insert(0, p_begin)
	points.append(p_end)

	res.extend(make_single_spline(points[0], points[1], points[2], points[3], 100, 1))

	for i in range(1, len(points) - 4):
		c = make_single_spline(points[i], points[i + 1], points[i + 2], points[i + 3], 100, 1)
		res.extend(c)

	res.extend(make_single_spline(points[len(points) - 4], points[len(points) - 3], 
								  points[len(points) - 2], points[len(points) - 1], 100, 1))

	points.remove(p_begin)
	points.remove(p_end)
	return res
