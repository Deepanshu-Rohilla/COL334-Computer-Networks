#ifndef TCPNEWRENOCSE
#define TCPNEWRENOCSE

#include "tcp-congestion-ops.h"

namespace ns3 {
class TcpNewRenoCSE : public TcpNewReno
{
public:
  static TypeId GetTypeId (void);
  std::string GetName () const;

protected:
  virtual uint32_t SlowStart (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
  virtual void CongestionAvoidance (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
};

} // namespace ns3

#endif // TCPCONGESTIONOPS_H
