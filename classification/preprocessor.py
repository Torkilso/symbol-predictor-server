import math
import numpy as np
from itertools import cycle

class Preprocessor:

    def __init__(self):
        pass


    def find_single_trace_distances(self, trace):
        # Finds distances between points in a trace

        trace_cycle = cycle(trace)
        next(trace_cycle)

        distances = []

        for point in trace[:-1]:
            next_point = next(trace_cycle)
            dist = math.hypot(next_point[0] - point[0], next_point[1] - point[1])
            distances.append(dist)
        return distances

    
    def add_points_to_trace(self, trace, goal):
        # Adds points to a trace until the amount of points = goal
        while len(trace) < goal:
            to_add = goal - len(trace)

            if to_add > len(trace):
                to_add = len(trace) - 1
            
            distances = self.find_single_trace_distances(trace)
            distances_index = [[j, i] for i, j in enumerate(distances)]
            sorted_distances_index = np.asarray(sorted(distances_index, reverse=True))
            
            try:
                for i in sorted_distances_index[0:to_add, 1]:
                    index = int(i)

                    new_x = (trace[index][0] + trace[index + 1][0]) / 2
                    new_y = (trace[index][1] + trace[index + 1][1]) / 2

                    trace = np.insert(trace, index+1, np.array((new_x, new_y)), axis=0)
            except IndexError:
                return trace

        return trace

    
    def find_overlap_pairs(self, traces):
        # Find the trace pairs that overlap

        overlap_pairs = set()

        traces_with_added_points = []

        center_values = []

        # Add points to all the traces
        for i, trace in enumerate(traces):
            new_trace = self.add_points_to_trace(trace, len(trace)*3)
            traces_with_added_points.append(new_trace)

        for trace in traces_with_added_points:
            center_values.append(((np.max(trace[:, 0]) + np.min(trace[:,0])) / 2, ((np.max(trace[:, 1]) + np.min(trace[:, 1])) / 2)))
        

        distances = []

        for i, values in enumerate(center_values):
            dist_calc = []

            for j, sec_value in enumerate(center_values):
                if j != i:
                    dist_calc.append([j, math.hypot(sec_value[0] - values[0], sec_value[1] - values[1])])

            sorted_dist = np.array(sorted(dist_calc, key=lambda tup: tup[1])[:6])

            distances.append(sorted_dist)


        for i, trace in enumerate(traces_with_added_points):

            counter = i
            for j, trace2 in enumerate(traces_with_added_points[i+1:]):
                counter += 1
                """
                for coord1 in trace:
                    if np.min(np.abs(trace2[:, 0] - coord1[0])) < 7 and np.min(np.abs(trace2[:, 1] - coord1[1])) < 7:
                        overlap_pairs.add((i, i+j+1))
                """
                """
                for coord1 in trace:
                    for coord2 in trace2:

                        # Calculate the distance
                        if math.hypot(coord2[0] - coord1[0], coord2[1] - coord1[1]) < 10:
                            overlap_pairs.add((i, counter))
                """
                if counter in distances[i][:, 0]:
                    
                    # Iterate through all possible pairs of points
                    for coord1 in trace:
                        for coord2 in trace2:

                            # Calculate the distance
                            if math.hypot(coord2[0] - coord1[0], coord2[1] - coord1[1]) < 10:
                                overlap_pairs.add((i, counter))
                
        return overlap_pairs

    
    def create_tracegroups(self, traces, trace_pairs):
        # Create group of traces based on pairs that overlap

        tracegroups = []
        for i, trace in enumerate(traces):

            flag = False
            for j, group in enumerate(tracegroups):

                common = []
                for p in trace_pairs:
                    if i in p:
                        common = common + list(p)
                common = list(set(common))

                if len(set(common).intersection(group)) > 0:
                     tracegroups[j] = list(set(common + group))
                     flag = True

            if not flag:
                new_group = [i]
                for pair in trace_pairs:
                    if i in pair:
                        new_group = new_group + list(pair)
                
                new_group = list(set(new_group))
                tracegroups.append(new_group)
            
        sorted_tracegroups = sorted(tracegroups, key=lambda m:next(iter(m)))
        return sorted_tracegroups
