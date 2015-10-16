#include <iostream>
#include <lemon/list_graph.h>
#include <lemon/preflow.h>
#include <limits.h>

using namespace lemon;

int main()
{
  ListDigraph g;

  auto s = g.addNode();
  auto t = g.addNode();

  auto m00 = g.addNode();
  auto m01 = g.addNode();
  auto m02 = g.addNode();
  auto m03 = g.addNode();
  auto m11 = g.addNode();
  auto m12 = g.addNode();

  lemon::ListDigraph::ArcMap<int> length(g);

  // Profitable blocks
  auto s_m00 = g.addArc(s, m00);
  auto s_m01 = g.addArc(s, m01);
  auto s_m11 = g.addArc(s, m11);
  length[s_m00] = 1;
  length[s_m01] = 1;
  length[s_m11] = 2;

  // Costly blocks
  auto t_m02 = g.addArc(m02, t);
  auto t_m03 = g.addArc(m03, t);
  auto t_m12 = g.addArc(t, m12);
  length[t_m02] = 1;
  length[t_m03] = 1;
  length[t_m12] = 1;

  // I'm guessing if I don't give a capacity, I get infinity?
  length[g.addArc(m11, m00)] = INT_MAX;
  length[g.addArc(m11, m01)] = INT_MAX;
  length[g.addArc(m11, m02)] = INT_MAX;
  length[g.addArc(m12, m01)] = INT_MAX;
  length[g.addArc(m12, m02)] = INT_MAX;
  length[g.addArc(m12, m03)] = INT_MAX;

  // Now call the min cut solver?
  auto preflower = Preflow<lemon::ListDigraph>(g, length, s, t);
  preflower.runMinCut();

  if (preflower.minCut(m00)) std::cout << "m00" << std::endl;
  if (preflower.minCut(m01)) std::cout << "m01" << std::endl;
  if (preflower.minCut(m02)) std::cout << "m02" << std::endl;
  if (preflower.minCut(m03)) std::cout << "m03" << std::endl;
  if (preflower.minCut(m11)) std::cout << "m11" << std::endl;
  if (preflower.minCut(m12)) std::cout << "m12" << std::endl;

  return 0;
}
