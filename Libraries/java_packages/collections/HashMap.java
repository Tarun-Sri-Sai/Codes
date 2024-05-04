package java_packages.collections;

import java.util.ArrayList;
import java.util.Collections;

public class HashMap<K, V> implements Map<K, V> {
    final int DEFAULT_CAPACITY = 10;
    int capacity, size;
    ArrayList<TreeMap<K, V>> hashTable;

    public HashMap() {
        capacity = DEFAULT_CAPACITY;
        size = 0;
        hashTable = new ArrayList<TreeMap<K, V>>(
                Collections.nCopies(capacity, null));
    }

    public void put(K key, V value) {
        Pair<K, V> prev = getPair(key);
        if (prev != null) {
            prev.value = value;
            return;
        }
        size++;
        int hashCode = hash(key);
        if (hashTable.get(hashCode) == null) {
            hashTable.set(hashCode, new TreeMap<>());
        }
        hashTable.get(hashCode).put(key, value);
        checkAndResize();
    }

    public boolean containsKey(K key) {
        int hashCode = hash(key);
        TreeMap<K, V> treeMap = hashTable.get(hashCode);
        if (treeMap == null) {
            return false;
        }
        if (treeMap.containsKey(key)) {
            return true;
        }
        return false;
    }

    public V get(K key) {
        Pair<K, V> result = getPair(key);
        if (result == null) {
            return null;
        }
        return result.value;
    }

    public V getOrDefault(K key, V defaultValue) {
        Pair<K, V> result = getPair(key);
        if (result == null) {
            return defaultValue;
        }
        return result.value;
    }

    private Pair<K, V> getPair(K key) {
        int hashCode = hash(key);
        TreeMap<K, V> treeMap = hashTable.get(hashCode);
        if (treeMap == null) {
            return null;
        }
        if (treeMap.containsKey(key)) {
            return new Pair<K, V>(
                    key,
                    treeMap.get(key));
        }
        return null;
    }

    public void remove(K key) {
        if (!containsKey(key)) {
            return;
        }
        size--;
        int hashCode = hash(key);
        TreeMap<K, V> treeMap = hashTable.get(hashCode);
        treeMap.remove(key);
        checkAndResize();
    }

    private void checkAndResize() {
        float loadValue = loadFactor();
        int prevSize = capacity;
        if (loadValue < 0.25) {
            capacity /= 2;
        }
        if (loadValue > 0.75) {
            capacity *= 2;
        }
        if (capacity <= DEFAULT_CAPACITY ||
                capacity == prevSize) {
            capacity = prevSize;
            return;
        }
        ArrayList<TreeMap<K, V>> newHashTable = new ArrayList<>(
                Collections.nCopies(capacity, null));
        for (int i = 0; i < prevSize; i++) {
            TreeMap<K, V> treeMap = hashTable.get(i);
            if (treeMap == null) {
                continue;
            }
            for (Pair<K, V> pair : treeMap) {
                int hashCode = hash(pair.key);
                if (newHashTable.get(hashCode) == null) {
                    newHashTable.set(hashCode, new TreeMap<>());
                }
                newHashTable.get(hashCode).put(
                        pair.key,
                        pair.value);
            }
        }
        hashTable = newHashTable;
    }

    private int hash(K key) {
        int result = (int) (((long) key.hashCode() + capacity) % capacity);
        while (result < 0 || result >= capacity) {
            result = (int) (((long) result + capacity) % capacity);
        }
        return result;
    }

    private float loadFactor() {
        return (float) size / capacity;
    }

    public void putIfAbsent(K key, V value) {
        if (!containsKey(key)) {
            put(key, value);
        }
    }

    public int size() {
        return size;
    }

    public void clear() {
        hashTable = new ArrayList<>(
                Collections.nCopies(DEFAULT_CAPACITY, null));
        capacity = DEFAULT_CAPACITY;
    }
}