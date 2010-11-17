program exemplo5 (input, ouput);
var n, k      : integer;
   f1, f2, f3 : integer;
   allan      : float;
begin
   read(n);
   f1:=0; f2:=0; k:=1;
   while k<=n do
   begin
      f3:= f1 + f2;
      f1:= f2;
      f2:= f3;
      k:=k+1;
   end;
   allan:=k;
   write(n,f1)
end.