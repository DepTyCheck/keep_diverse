// Seed: 7475688735560469961,5224943229413370507

module uw
  ( output realtime bkt [1:2][1:4]
  , output bit [1:0][2:3][0:0][0:2]  wez
  , output trireg logic [0:0][4:1][0:4] qectwj [3:2][0:3][3:4][2:2]
  , input triand logic emsbgwm [3:1]
  , input shortreal sigttowtre [1:2]
  , input trior logic [0:4][0:2]  bfpr
  );
  
  
  not iahgjfma(s, wez);
  // warning: implicit conversion of port connection truncates from 12 to 1 bits
  // warning: implicit conversion changes possible bit states from 2-state to 4-state
  //   bit [1:0][2:3][0:0][0:2]  wez -> logic wez
  
  not pujphoxd(ekvtjwfku, bfpr);
  // warning: implicit conversion of port connection truncates from 15 to 1 bits
  //   trior logic [0:4][0:2]  bfpr -> logic bfpr
  
  or aagnoljg(wez, it, bfpr);
  // warning: implicit conversion of port connection expands from 1 to 12 bits
  // warning: implicit conversion changes possible bit states from 4-state to 2-state
  //   logic wez -> bit [1:0][2:3][0:0][0:2]  wez
  //
  // warning: implicit conversion of port connection truncates from 15 to 1 bits
  //   trior logic [0:4][0:2]  bfpr -> logic bfpr
  
  nand qzif(c, it, wez);
  // warning: implicit conversion of port connection truncates from 12 to 1 bits
  // warning: implicit conversion changes possible bit states from 2-state to 4-state
  //   bit [1:0][2:3][0:0][0:2]  wez -> logic wez
  
  
  // Single-driven assigns
  assign bkt = bkt;
  
  // Multi-driven assigns
  assign qectwj = qectwj;
  assign s = wez;
  assign ekvtjwfku = wez;
  assign c = 'b1x0;
endmodule: uw



// Seed after: 4710340899852046314,5224943229413370507
