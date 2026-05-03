// Seed: 8037307645434483667,5224943229413370507

module gq
  ( output logic hikhv [4:1]
  , output supply0 logic gkpub [4:3][2:3][3:2][2:0]
  , output supply1 logic [2:4][4:3][2:0][2:3] ieubpov [3:4][3:4]
  , input wand logic [1:4]  nmo
  , input uwire logic [0:4] zdtdjoyz [1:3][0:2][0:3]
  , input triand logic g [2:4][0:4][4:2]
  , input tri logic [4:2] gpjnea [3:4]
  );
  
  
  and rwlppku(unofqxul, nmo, eoxzxtee);
  // warning: implicit conversion of port connection truncates from 4 to 1 bits
  //   wand logic [1:4]  nmo -> logic nmo
  
  or vr(nmo, nmo, unofqxul);
  // warning: implicit conversion of port connection expands from 1 to 4 bits
  //   logic nmo -> wand logic [1:4]  nmo
  //
  // warning: implicit conversion of port connection truncates from 4 to 1 bits
  //   wand logic [1:4]  nmo -> logic nmo
  
  or jfpojqac(nmo, unofqxul, nmo);
  // warning: implicit conversion of port connection expands from 1 to 4 bits
  //   logic nmo -> wand logic [1:4]  nmo
  //
  // warning: implicit conversion of port connection truncates from 4 to 1 bits
  //   wand logic [1:4]  nmo -> logic nmo
  
  
  // Single-driven assigns
  assign hikhv = hikhv;
  
  // Multi-driven assigns
  assign eoxzxtee = unofqxul;
  assign ieubpov = ieubpov;
  assign gkpub = '{'{'{'{'b1x,'b1001,'bx01},'{'bx0,'b11z0,'bx0xx}},'{'{'bzzzx,'bx0,'b1},'{'b0,'bz01z1,'b1z10}}},'{'{'{'bxz0z,'b10000,'b1xz},'{'bxxzz,'b1,'bz0111}},'{'{'bxz1,'bz1,'bx0z0},'{'b01,'b0xx0,'b110xz}}}};
  assign unofqxul = 'b0x0xx;
endmodule: gq

module vxes
  (output logic [0:2][3:0][1:1]  b, output bit f, output shortreal wmdgas, input triand logic [1:3][4:4] sh [3:2][0:0]);
  
  
  nand aymulnxmmm(b, wmdgas, b);
  // warning: implicit conversion of port connection expands from 1 to 12 bits
  //   logic b -> logic [0:2][3:0][1:1]  b
  //
  // warning: implicit conversion of port connection truncates from 32 to 1 bits
  // warning: implicit conversion changes signedness from signed to unsigned
  //   shortreal wmdgas -> logic wmdgas
  //
  // warning: implicit conversion of port connection truncates from 12 to 1 bits
  //   logic [0:2][3:0][1:1]  b -> logic b
  
  
  // Single-driven assigns
  assign f = b;
  assign wmdgas = f;
  
  // Multi-driven assigns
  assign sh = sh;
endmodule: vxes

module k
  (output trireg logic [2:4] ob [2:2][1:4][1:3], input wor logic mc [3:2][4:1][0:1]);
  
  supply1 logic [2:4][4:3][2:0][2:3] natcrjwkzq [3:4][3:4];
  supply0 logic w [4:3][2:3][3:2][2:0];
  logic hah [4:1];
  tri logic [4:2] rmvkgoq [3:4];
  triand logic nn [2:4][0:4][4:2];
  uwire logic [0:4] eamk [1:3][0:2][0:3];
  triand logic [1:3][4:4] g [3:2][0:0];
  
  vxes y(.b(cxbgyrll), .f(chlctvcwbu), .wmdgas(chlctvcwbu), .sh(g));
  // warning: implicit conversion of port connection truncates from 12 to 1 bits
  //   logic [0:2][3:0][1:1]  b -> wire logic cxbgyrll
  //
  // warning: implicit conversion changes possible bit states from 2-state to 4-state
  //   bit f -> wire logic chlctvcwbu
  //
  // warning: implicit conversion of port connection truncates from 32 to 1 bits
  // warning: implicit conversion changes signedness from signed to unsigned
  //   shortreal wmdgas -> wire logic chlctvcwbu
  
  gq qrdzgr(.hikhv(hah), .gkpub(w), .ieubpov(natcrjwkzq), .nmo(chlctvcwbu), .zdtdjoyz(eamk), .g(nn), .gpjnea(rmvkgoq));
  // warning: implicit conversion of port connection expands from 1 to 4 bits
  //   wire logic chlctvcwbu -> wand logic [1:4]  nmo
  
  
  // Single-driven assigns
  assign eamk = '{'{'{'{'bz,'b11x,'b0z1z,'bz,'bxx0},'{'bz0,'bx0,'bx0,'b0x1x1,'bzxzz},'{'bz101,'bx0z00,'b1zxz,'bzxz0z,'b10},'{'bzz1x,'b1x0x1,'b0001,'bz,'b101z0}},'{'{'bxz,'b1zx,'bzzz,'b1111x,'b1},'{'b0z0,'bx1,'b1z11,'b0,'bx1},'{'bx1z0z,'bx,'bx,'b1z0,'bxzzxx},'{'b1zz,'b010,'bz1x,'bxx1,'b0}},'{'{'b1z0,'bzz11,'bz0x,'b0xx,'b0xx},'{'bxx,'bxz,'b1001,'b1,'bzx0z},'{'bx00,'bz,'bx,'b1zz,'bz11},'{'bx1xz,'bxz0,'b0zzz,'b0,'bx0z0x}}},'{'{'{'b1011,'bx,'b111z,'bx,'bzz1x},'{'bz,'bz,'bzx1,'b1z,'bxz1x},'{'bxx011,'bx0zx,'bz,'b0,'bzx},'{'bz1,'bz0111,'b01zz,'bz10xx,'bzz}},'{'{'bzx,'b000,'bxx,'b1,'bx110},'{'b100,'bx1,'b10,'bzz0,'bzz0},'{'b1000,'bzz0,'bx,'b01x1,'b0zx},'{'b001z,'b1xx01,'b0x,'bx,'b1z}},'{'{'bzz,'bx1,'b0z1z,'b111x,'bx01},'{'bxx,'b0zzz,'bz,'bx10x,'bx1xxx},'{'b1,'b0,'b101,'b1001z,'b011zz},'{'bz00z,'b0z,'bz1,'b00,'b0xx01}}},'{'{'{'b000,'bz1x1,'bz00,'b1z,'bx},'{'bz,'b0x,'bz,'b001z0,'b100z},'{'b0,'bx1,'b00,'b1,'b0x0},'{'bz,'b1z1x,'bx0,'b0z,'bz110x}},'{'{'b10,'b110xz,'b1z0z,'bz,'bx0},'{'b1,'b0x1xz,'b01,'bxz,'b0},'{'b0x0,'bzxz1z,'b1x11z,'b100zz,'b1},'{'b1x,'b10z,'b0,'b0z,'bz10z}},'{'{'bz10x,'b1,'b100x1,'bz1zx,'b00000},'{'b0z,'b0,'bzxx,'bzxx,'b1x0},'{'bzz1x,'b0,'b111,'b0,'b101},'{'b0zx,'b0zxz,'bx,'b1z,'bxz}}}};
  
  // Multi-driven assigns
  assign ob = '{'{'{'{'b10x1,'b1xz0,'b00},'{'bz11zx,'b0xxz1,'bx10},'{'b1x1x1,'bxx1xz,'b00}},'{'{'b0x0x,'bz1x01,'bxx},'{'b1x,'bz,'bz},'{'b0x11x,'bx10,'bx001}},'{'{'bx0z1,'b0xxxx,'bx11x},'{'b1z0zx,'b01z,'bx},'{'b1010,'b00,'bzzz}},'{'{'b1zx0,'b0x0,'bx},'{'bzz,'b01z,'b01z},'{'b1zxz,'b01z1,'bxz00}}}};
  assign nn = nn;
  assign cxbgyrll = 'bx00;
  assign chlctvcwbu = 'bx0;
  assign w = w;
endmodule: k

module o
  ( output tri logic i [4:4]
  , output supply1 logic [3:0][2:1][3:2] e [3:2][1:3][3:2]
  , output reg [0:1][4:0][4:4]  mmaajnf
  , input supply0 logic [2:4] ylizrwt [1:3]
  , input supply0 logic cdcwegakax [3:4]
  );
  
  supply1 logic [2:4][4:3][2:0][2:3] zehnucsxtp [3:4][3:4];
  supply0 logic mnwkz [4:3][2:3][3:2][2:0];
  logic ubslvgl [4:1];
  tri logic [4:2] cpt [3:4];
  triand logic hla [2:4][0:4][4:2];
  uwire logic [0:4] o [1:3][0:2][0:3];
  
  gq pqrmowvu(.hikhv(ubslvgl), .gkpub(mnwkz), .ieubpov(zehnucsxtp), .nmo(mmaajnf), .zdtdjoyz(o), .g(hla), .gpjnea(cpt));
  // warning: implicit conversion of port connection truncates from 10 to 4 bits
  //   reg [0:1][4:0][4:4]  mmaajnf -> wand logic [1:4]  nmo
  
  or ju(mmaajnf, mmaajnf, mmaajnf);
  // warning: implicit conversion of port connection expands from 1 to 10 bits
  //   logic mmaajnf -> reg [0:1][4:0][4:4]  mmaajnf
  //
  // warning: implicit conversion of port connection truncates from 10 to 1 bits
  //   reg [0:1][4:0][4:4]  mmaajnf -> logic mmaajnf
  //
  // warning: implicit conversion of port connection truncates from 10 to 1 bits
  //   reg [0:1][4:0][4:4]  mmaajnf -> logic mmaajnf
  
  
  // Single-driven assigns
  assign o = '{'{'{'{'b00,'b0xxx,'bz,'bx0xx,'bz0},'{'bz0z,'b00,'b01xz,'b01x,'bz},'{'b0zxz,'bx111,'bz1x1,'b11,'b1111},'{'b111,'bx10,'b00,'bzz,'bzx}},'{'{'b100,'bz011,'b100,'b0x1x,'bx1},'{'bz,'bxx,'bxz1,'bx10xz,'b0z},'{'bzx0,'bx,'b1zz1,'b1,'b0z1},'{'bx0z1,'bx0101,'b0,'bzx0x,'b1x1x0}},'{'{'bx1z,'bz1zzx,'bxzx,'b10z,'b1zxz1},'{'bxzz,'bz1111,'bz,'bz,'b10x01},'{'bzx,'b01,'b0011x,'bz,'bxz0},'{'bz,'b101,'bx,'bxz,'b1z}}},'{'{'{'b0,'bz0,'bx11,'b10,'bz1z},'{'b0x010,'b00xxz,'b1,'bxxz,'bx10z},'{'b10,'b0,'b1xx,'bx110,'b000},'{'b1,'bxz,'bx,'bxx00,'b0zz}},'{'{'bxxz,'b0x,'bx1xz,'bx,'b10},'{'bzx,'bx,'b1x,'bz,'b1},'{'b1,'bzxz1,'b00,'b00x1x,'b1xx1},'{'bx1011,'bz000,'bxx,'b1,'b1xz}},'{'{'bxx0,'bz101,'b0z0z,'bx1,'b0x},'{'b1z1x,'b0z0,'bz,'b10x,'bz0},'{'b1z,'bz,'bzxxz,'b00,'bxx1},'{'b010,'bx1zz0,'b0,'bz00,'b1xx}}},'{'{'{'bzzx,'b0,'bzxz0,'b111zx,'bzzz0},'{'b0010x,'b101xz,'b1011,'b1x,'b0},'{'b1zx,'bx00zx,'b10,'bx,'b0z},'{'bxxzz,'b0z01,'bx0,'bz1x,'b11z10}},'{'{'bzz,'b01xx1,'b1xx,'b00xz,'bx},'{'bz1z,'bz1x01,'b0z1z,'b0x1x,'bzx11},'{'b10x,'b0x,'b1xx0,'b0z,'bz01x},'{'bx,'bzx0xx,'bxz0,'bzx,'bz}},'{'{'bxzx0,'bz,'b11xx,'bxz0,'b0zx00},'{'b1,'bxx10,'b0x0z,'bxzz,'b1xzx0},'{'b1x0,'bzzz1,'b1z10,'b1,'bz1z1},'{'b0xzx0,'bx,'b00z,'b111,'bx0x0}}}};
  
  // Multi-driven assigns
  assign i = '{'b1x};
  assign zehnucsxtp = zehnucsxtp;
endmodule: o



// Seed after: 11054676645773098073,5224943229413370507
