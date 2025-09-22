try:
    import tensorflow.lite
    print("TensorFlow Lite is available.")
except ImportError:
    print("TensorFlow Lite is not available.")
