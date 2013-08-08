#ifndef ASYNC_SAMPLE_COLLECTOR_HPP
#define ASYNC_SAMPLE_COLLECTOR_HPP

#include <boost/lockfree/spsc_queue.hpp>
#include <boost/atomic.hpp>
#include <cstddef>

#include "Bci.hpp"
#include "Sample.hpp"
#include "SampleBuffer.hpp"

using namespace boost;

class AsyncSampleCollector
{
public:
  AsyncSampleCollector(Bci* pBci, lockfree::spsc_queue<Sample<uint32_t>*, lockfree::capacity<(SAMPLE_BUFFER_SIZE-1)> >* pQueue,
		       atomic<bool>* pDone, Sample<uint32_t>* pSamples, SampleBuffer<uint32_t>* pRingBuffer);
  
  AsyncSampleCollector(const AsyncSampleCollector& copy);
  ~AsyncSampleCollector();
  
public:
  AsyncSampleCollector& operator=(const AsyncSampleCollector& other);
  void operator()();
  
private:
  Bci* mpBci;
  spsc_queue<Sample<uint32_t>*, capacity<(SAMPLE_BUFFER_SIZE-1)> >* mpQueue;
  atomic<bool>* mpDone;
  Sample<uint32_t>* mpSamples;
  SampleBuffer<uint32_t>* mpRingBuffer;
  size_t mCurrentSample;
};

#endif