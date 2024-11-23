package java_packages.collections;

import java.util.ArrayList;
import java.util.Comparator;

public class PriorityQueue<T> {
    private ArrayList<T> heapList;
    private Comparator<T> prioritizer;
    private int size;

    public PriorityQueue(Comparator<T> prioritizer) {
        heapList = new ArrayList<>();
        this.prioritizer = prioritizer;
        size = 0;
    }

    public void add(T ele) {
        heapList.add(ele);
        size++;
        int child = size - 1, parent;
        while ((parent = parent(child)) > -1 && prioritizer.compare(heapList.get(parent), heapList.get(child)) > 0) {
            swap(parent, child);
            child = parent;
        }
    }

    public T peek() {
        return size <= 0 ? null : heapList.get(0);
    }

    public T remove() {
        if (size <= 0) {
            return null;
        }
        T result = heapList.get(0);
        heapList.set(0, heapList.get(size - 1));
        heapList.remove(size - 1);
        size--;
        int valid = 0, curr = 0;
        while (curr < size) {
            valid = curr;
            int leftChild = leftChild(curr), rightChild = rightChild(curr);
            if (leftChild > -1 && prioritizer.compare(heapList.get(valid), heapList.get(leftChild)) > 0) {
                valid = leftChild(curr);
            }
            if (rightChild > -1 && prioritizer.compare(heapList.get(valid), heapList.get(rightChild)) > 0) {
                valid = rightChild(curr);
            }
            if (valid == curr) {
                break;
            }
            swap(valid, curr);
            curr = valid;
        }
        return result;
    }

    public int size() {
        return size;
    }

    private void swap(int parent, int curr) {
        T temp = heapList.get(parent);
        heapList.set(parent, heapList.get(curr));
        heapList.set(curr, temp);
    }

    private int parent(int child) {
        if (child <= 0) {
            return -1;
        }
        return (child - 1) / 2;
    }

    private int leftChild(int parent) {
        int result = parent * 2 + 1;
        return result >= size ? -1 : result;
    }

    private int rightChild(int parent) {
        int result = parent * 2 + 2;
        return result >= size ? -1 : result;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < size; i++) {
            sb.append((heapList.get(i) + ""));
            if (i < size - 1) {
                sb.append(", ");
            }
        }
        sb.append("]");
        String result = sb.toString();
        return result;
    }
}