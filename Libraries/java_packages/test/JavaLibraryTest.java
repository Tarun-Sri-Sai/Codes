package java_packages.test;

public class JavaLibraryTest {
    public static void main(String[] args) throws java.lang.Exception {
        for (int n = 1; n <= 4; n++) {
            long startTime = System.currentTimeMillis();
            switch (n) {
                case 1: { // HashMap Default Implementation
                    java.util.Map<Integer, Integer> map = new java.util.HashMap<>();
                    for (int i = 0; i < (int) 1e3; i++) {
                        map.put(i, i * i);
                    }
                    for (int i = 0; i < (int) 1e3; i++) {
                        System.out.print("\r" + (map.containsKey(i) ? map.get(i) : ":("));
                    }
                    break;
                }
                case 2: { // HashMap My Implementation
                    java_packages.collections.Map<Integer, Integer> map = new java_packages.collections.HashMap<>();
                    for (int i = 0; i < (int) 1e3; i++) {
                        map.put(i, i * i);
                    }
                    for (int i = 0; i < (int) 1e3; i++) {
                        System.out.print("\r" + (map.containsKey(i) ? map.get(i) : ":("));
                    }
                    break;
                }
                case 3: { // TreeMap Default Implementation
                    java.util.Map<Integer, Integer> map = new java.util.TreeMap<>();
                    for (int i = 0; i < (int) 1e3; i++) {
                        map.put(i, i * i);
                    }
                    for (int i = 0; i < (int) 1e3; i++) {
                        System.out.print("\r" + (map.containsKey(i) ? map.get(i) : ":("));
                    }
                    break;
                }
                case 4: { // TreeMap My Implementation
                    java_packages.collections.Map<Integer, Integer> map = new java_packages.collections.TreeMap<Integer, Integer>();
                    for (int i = 0; i < (int) 1e3; i++) {
                        map.put(i, i * i);
                    }
                    for (int i = 0; i < (int) 1e3; i++) {
                        System.out.print("\r" + (map.containsKey(i) ? map.get(i) : ":("));
                    }
                    break;
                }
                default:
                    return;
            }
            long endTime = System.currentTimeMillis();
            Runtime runtime = Runtime.getRuntime();
            long memory = (runtime.totalMemory() - runtime.freeMemory()) / 1024L;
            switch (n) {
                case 1: { // HashMap Default Implementation
                    System.out.println("\rDefault HashMap: " + memory + " KB");
                    break;
                }
                case 2: { // HashMap My Implementation
                    System.out.println("\rMy HashMap: " + memory + " KB");
                    break;
                }
                case 3: { // TreeMap Default Implementation
                    System.out.println("\rDefault TreeMap: " + memory + " KB");
                    break;
                }
                case 4: { // TreeMap My Implementation
                    System.out.println("\rMy TreeMap: " + memory + " KB");
                    break;
                }
                default:
                    return;
            }
            System.out.println("Time consumed: " + (endTime - startTime) + " ms");
            if (n < 4) System.out.println();
        }
    }
}