import java.util.Random;
import java.util.Arrays;
import java.util.Comparator;

public class HeapSort {
    public static void main(String[] args) {
        int iters = 1000;
        int minSize = 10, maxSize = 15;
        int minRange = 0, maxRange = 100;
        for (int i = 0; i < iters; i++) {
            Integer[] arr = getRandomIntArray(minSize, maxSize, minRange, maxRange);
            Comparator<Integer> cmp = (i1, i2) -> i1 - i2;
            heapSort(arr, cmp);
            if (!isSorted(arr, cmp)) {
                System.out.println("Problem with heap sort " + Arrays.toString(arr));
                return;
            }
        }
        System.out.println(iters + " arrays sorted");
    }

    private static <T> boolean isSorted(T[] arr, Comparator<T> cmp) {
        int size = arr.length;
        for (int i = 0; i < size - 1; i++) {
            if (cmp.compare(arr[i], arr[i + 1]) > 0) {
                return false;
            }
        }
        return true;
    }

    private static <T> void heapSort(T[] arr, Comparator<T> cmp) {
        int size = arr.length;
        for (int i = size / 2 - 1; i >= 0; i--) {
            heapifyDown(arr, size, i, cmp);
        }
        for (int i = size - 1; i >= 0; i--) {
            swap(arr, 0, i);
            heapifyDown(arr, i, 0, cmp);
        }
    }

    private static <T> void heapifyDown(T[] arr, int size, int firstIndex, Comparator<T> cmp) {
        int parent = firstIndex;
        while (parent < size) {
            int prev = parent, left = 2 * parent + 1, right = left + 1;
            if (left < size && cmp.compare(arr[left], arr[parent]) >= 0) {
                parent = left;
            }
            if (right < size && cmp.compare(arr[right], arr[parent]) >= 0) {
                parent = right;
            }
            if (parent == prev) {
                return;
            }
            swap(arr, parent, prev);
        }
    }

    private static <T> void swap(T[] arr, int first, int second) {
        T temp = arr[first];
        arr[first] = arr[second];
        arr[second] = temp;
    }

    private static Integer[] getRandomIntArray(int minSize, int maxSize, int minRange, int maxRange) {
        int size = boundedRandom(minSize, maxSize);
        Integer[] result = new Integer[size];
        for (int i = 0; i < size; i++) {
            result[i] = boundedRandom(minRange, maxRange);
        }
        return result;
    }

    private static int boundedRandom(int lowerBound, int upperBound) {
        Random random = new Random(System.currentTimeMillis());
        return lowerBound + random.nextInt(upperBound - lowerBound + 1);
    }
}
