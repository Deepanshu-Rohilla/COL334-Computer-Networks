#include "TcpNewRenoCSE.h"
#include "ns3/log.h"

namespace ns3 {

NS_OBJECT_ENSURE_REGISTERED (TcpNewRenoCSE);

TypeId
TcpNewRenoCSE::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::TcpNewRenoCSE")
    .SetParent<TcpNewReno> ()
    .SetGroupName ("Internet")
    .AddConstructor<TcpNewRenoCSE> ()
  ;
  return tid;
}
uint32_t
TcpNewRenoCSE::SlowStart (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{

  if (segmentsAcked >= 1)
    {
      tcb->m_cWnd += static_cast<uint32_t> (static_cast<double> (std::pow(tcb->m_segmentSize, 1.9))/tcb->m_cWnd);
      return segmentsAcked - 1;
    }

  return 0;
}
void
TcpNewRenoCSE::CongestionAvoidance (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{

  if (segmentsAcked > 0)
    {
      double adder = static_cast<double> (0.5*(tcb->m_segmentSize));
      adder = std::max (1.0, adder);
      tcb->m_cWnd = tcb->m_cWnd + static_cast<uint32_t> (adder);
    }
}
std::string
TcpNewRenoCSE::GetName () const
{
  return "TcpNewRenoCSE";
}
}