package java_packages.collections;

public interface Map<K, V> {
    public void put(K key, V value);

    public V get(K key);

    public boolean containsKey(K key);

    public V getOrDefault(K key, V defaultValue);

    public void putIfAbsent(K key, V value);

    public void remove(K key);

    public int size();

    public void clear();
}