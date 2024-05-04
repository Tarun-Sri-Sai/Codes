import java.io.*;
import java.util.*;

public class Dijkstra {
    private static Scanner sc;
    private static BufferedWriter bw;
    private static final int MAX_SIZE = 0x100, INFINITY = Integer.MAX_VALUE;
    private static Random random = new Random(System.currentTimeMillis());

    public static void main(String[] args) throws IOException {
        sc = new Scanner(System.in);
        bw = new BufferedWriter(new OutputStreamWriter(System.out));
        int[][] adj = new int[MAX_SIZE][MAX_SIZE];
        int length = 4 + random.nextInt(4);
        if (length > 26) {
            return;
        }
        char[] vertexNames = generateVertices(length);
        for (char startVertex : vertexNames) {
            for (char endVertex : vertexNames) {
                adj[startVertex][endVertex] = (startVertex == endVertex ? 0 : random.nextInt(10));
            }
        }
        bw.write("Number of vertices: " + vertexNames.length + "\n");
        bw.write("Adjacency Matrix is:\n");
        printMatrix(adj, vertexNames);
        Distance[] visited = dijkstra(adj, vertexNames);
        bw.write("------------------------------------------------------\n");
        for (char vertex : vertexNames) {
            bw.write("Vertex: " + visited[vertex].vertex + " -> " + numberOrInfinity(visited[vertex].distance) + "\n");
        }
        sc.close();
        bw.flush();
    }

    private static String numberOrInfinity(int distance) {
        return (distance == INFINITY ? "INF" : distance) + "";
    }

    private static char[] generateVertices(int length) {
        List<Character> chars = new ArrayList<>();
        for (int i = 0; i < length; i++) {
            chars.add((char) ('A' + i));
        }
        char[] result = new char[length];
        for (int i = 0; i < length; i++) {
            result[i] = chars.get(i);
        }
        return result;
    }

    private static Distance[] dijkstra(int[][] adj, char[] vertexNames) throws IOException {
        PriorityQueue<Distance> pq = new PriorityQueue<>(new Prioritizer());
        Distance[] vertices = new Distance[MAX_SIZE];
        for (char vertex : vertexNames) {
            vertices[vertex] = new Distance(vertex, INFINITY);
        }
        int length = vertexNames.length;
        char start = (char) ('A' + random.nextInt(length));
        bw.write("Chosen vertex: " + start + "\n");
        vertices[start].distance = 0;
        pq.add(vertices[start]);
        List<Character> visited = new ArrayList<>();
        while (visited.size() < length) {
            Distance curr = pq.remove();
            if (curr == null) {
                bw.write("One or more vertices are unreachable!\n");
                break;
            }
            bw.write("Current popped: " + curr + "\n");
            char popped = curr.vertex;
            for (char vertex : vertexNames) {
                if (adj[popped][vertex] != 0) {
                    int relaxedDistance = vertices[popped].distance + adj[popped][vertex];
                    if (relaxedDistance < vertices[vertex].distance) {
                        vertices[vertex].distance = relaxedDistance;
                        pq.add(vertices[vertex]);
                    }
                }
            }
            bw.write("Priority Queue: " + pq + "\n");
            visited.add(popped);
        }
        return vertices;
    }

    private static void printMatrix(int[][] adj, char[] vertexNames) throws IOException {
        for (char vertex : vertexNames) {
            bw.write("\t" + vertex);
        }
        bw.write("\n\n");
        for (char startVertex : vertexNames) {
            bw.write(startVertex + "\t");
            for (char endVertex : vertexNames) {
                bw.write(adj[startVertex][endVertex] + "\t");
            }
            bw.write("\n\n");
        }
    }
}

class Distance {
    char vertex;
    int distance;

    public Distance(char vertex, int distance) {
        this.vertex = vertex;
        this.distance = distance;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder("(");
        sb.append(vertex + ", ");
        sb.append(distance + ")");
        String result = sb.toString();
        return result;
    }
}

class Prioritizer implements Comparator<Distance> {
    @Override
    public int compare(Distance d1, Distance d2) {
        return d1.distance - d2.distance;
    }
}