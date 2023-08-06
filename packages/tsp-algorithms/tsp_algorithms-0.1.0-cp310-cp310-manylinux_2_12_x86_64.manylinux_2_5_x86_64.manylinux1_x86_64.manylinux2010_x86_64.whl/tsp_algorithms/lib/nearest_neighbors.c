#include <stdlib.h>

#include "./include/nearest_neighbors.h"


// Calculate the route cost given a cost matrix
float route_cost(float **cost_matrix, int *route, int n){
    float cost = 0;
    for (int i = 0; i < n; i++){
        cost += cost_matrix[route[i]][route[(i+1)%n]];
    }
    return cost;
};

// Wrapper to generate a route using the nearest neighbor algorithm
int *nearest_neighbors(float **cost_matrix, int n){
    int *route = (int *)malloc(n * sizeof(int));
    int *current_route = (int *)malloc(n * sizeof(int));
    int *visited = (int *)malloc(n * sizeof(int));

    float path_fitness = 1000000000;
    for (int starting_node = 0; starting_node < n; starting_node++){
        for (int i = 0; i < n; i++){
            visited[i] = 0;
        }
        int current_node = starting_node;
        for (int i = 0; i < n; i++){
            current_route[i] = current_node;
            visited[current_node] = 1;
            float min_cost = 1000000000;
            int min_node = -1;
            for (int j = 0; j < n; j++){
                if (visited[j] == 0 && cost_matrix[current_node][j] < min_cost){
                    min_cost = cost_matrix[current_node][j];
                    min_node = j;
                }
            }
            current_node = min_node;
        }
        float current_fitness = route_cost(cost_matrix, current_route, n);
        if (current_fitness < path_fitness){
            path_fitness = current_fitness;
            for (int i = 0; i < n; i++){
                route[i] = current_route[i];
            }
        }
    }
    return route;
};
