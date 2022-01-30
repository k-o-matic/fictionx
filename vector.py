class Vector2:

    def sum(a, b):
        result = list(map(sum, zip(a, b)))
        return result

    def subtract(origin, target):
        result = []
        result.append(origin[0] - target[0])
        result.append(origin[1] - target[1])
        return result

    def y_target_factor(origin, target):
        #new_vector = list(map(operator.sub, origin, target))
        new_vector = []
        new_vector.append(origin[0] - target[0])
        new_vector.append(origin[1] - target[1])
        result = new_vector[1] / new_vector[0]
        return result