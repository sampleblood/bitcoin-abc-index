
#ifndef BITCOIN_TIMESTAMPINDEX_H
#define BITCOIN_TIMESTAMPINDEX_H

#include <uint256.h>

struct CTimestampIndexIteratorKey {
    unsigned int timestamp;

    size_t GetSerializeSize() const { return 4; }
    template <typename Stream> void Serialize(Stream &s) const {
        ser_writedata32be(s, timestamp);
    }
    template <typename Stream> void Unserialize(Stream &s) {
        timestamp = ser_readdata32be(s);
    }

    CTimestampIndexIteratorKey(unsigned int time) { timestamp = time; }

    CTimestampIndexIteratorKey() { SetNull(); }

    void SetNull() { timestamp = 0; }
};

struct CTimestampIndexKey {
    unsigned int timestamp;
    BlockHash blockHash;

    size_t GetSerializeSize() const { return 36; }
    template <typename Stream> void Serialize(Stream &s) const {
        ser_writedata32be(s, timestamp);
        blockHash.Serialize(s);
    }
    template <typename Stream> void Unserialize(Stream &s) {
        timestamp = ser_readdata32be(s);
        blockHash.Unserialize(s);
    }

    CTimestampIndexKey(unsigned int time, BlockHash hash) {
        timestamp = time;
        blockHash = hash;
    }

    CTimestampIndexKey() { SetNull(); }

    void SetNull() {
        timestamp = 0;
        blockHash.SetNull();
    }
};

struct CTimestampBlockIndexKey {
    uint256 blockHash;

    size_t GetSerializeSize() const { return 32; }

    template <typename Stream> void Serialize(Stream &s) const {
        blockHash.Serialize(s);
    }

    template <typename Stream> void Unserialize(Stream &s) {
        blockHash.Unserialize(s);
    }

    CTimestampBlockIndexKey(uint256 hash) { blockHash = hash; }

    CTimestampBlockIndexKey() { SetNull(); }

    void SetNull() { blockHash.SetNull(); }
};

struct CTimestampBlockIndexValue {
    unsigned int ltimestamp;
    size_t GetSerializeSize() const { return 4; }

    template <typename Stream> void Serialize(Stream &s) const {
        ser_writedata32be(s, ltimestamp);
    }

    template <typename Stream> void Unserialize(Stream &s) {
        ltimestamp = ser_readdata32be(s);
    }

    CTimestampBlockIndexValue(unsigned int time) { ltimestamp = time; }

    CTimestampBlockIndexValue() { SetNull(); }

    void SetNull() { ltimestamp = 0; }
};

#endif // BITCOIN_TIMESTAMPINDEX_H