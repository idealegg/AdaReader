-----------------------------------------------------------------------------
-- Copyright (C) 2001 Thales ATM all rights reserved. This software is the --
-- property of Thales ATM and may not be used in any manner except under a --
-- licence agreement signed with Thales ATM.                               --
-----------------------------------------------------------------------------
-- 
--  LIBRARY UNIT NAME :    STANDARD_TYPES
-- 
--  SOURCE FILENAME :      standard_types.a
-- 
--  FUNCTION :		Redefinition of machine implementation
--			dependent types.
-- 
--  SEPARATE UNITS :   None
-- 
--  DESIGNERS :        Hans Boon, Jacques Edeline, Dick de Rond
--                     Darjo J. Dominique
--
--  VERSION   :        mai#4.3
-- 
--  COMMENTS :	       This package is compiler dependent and has to
--		       be adapted.
-- 
-----------------------------------------------------------------------
--   SPACF   DATE   CORRECTOR       DESIGNATION
-----------------------------------------------------------------------
-- V3.3
--   PCR709 12/11/96  AML       Port to solaris 
--                                -> Dec5, HP-UX, Solaris with Alpha interface
--   PCR788 21/11/96  AML       Bad definition in the new Dec5,HP-UX,Solaris interface.
--
-- V3.4
--   PCR941 17/04/97  AML       Port to HP-UX 10.x : Ada Verdix float on 32 bits.
-- V3.11
--   ECR_4  28/08/01  LD	Port to HP-UX 11.x 64 bits
--   PCR_131 14/01/02 LD        Define INTEGER_64 and derived types with  1 
--   PCR_641 05/09/02 LD        Define UNSIGNED_32 type with  1  as on Alpha
-----------------------------------------------------------------------

package STANDARD_TYPES is

  -- SPMS+ file identification
  SCCS_STANDARD_TYPES : constant STRING :=
    "@(#) UBSS standard_types.common MISC:39-797-384 : mai#4.3 : 05-SEP-2002 15:07:11 ~";

  OCTET : constant := 8;
  SHORT : constant := 16;
  WORD  : constant := 32;

  type INTEGER_8 is  new INTEGER    range -(2 ** 7)  .. (2 ** 7)  - 1;
  for  INTEGER_8'SIZE use 8;

  type INTEGER_16 is new INTEGER    range -(2 ** 15) .. (2 ** 15) - 1;
  for  INTEGER_16'SIZE use 16;

  subtype INTEGER_32 is INTEGER;

  type INTEGER_64 is range
      -9_223_372_036_854_775_808 .. 9_223_372_036_854_775_807;
  for INTEGER_64'SIZE use 64;

  subtype NATURAL_8  is INTEGER_8   range 0 .. INTEGER_8'LAST;

  subtype NATURAL_16 is INTEGER_16  range 0 .. INTEGER_16'LAST;

  subtype NATURAL_32 is INTEGER_32  range 0 .. INTEGER_32'LAST;

  subtype NATURAL_64 is INTEGER_64  range 0 .. INTEGER_64'LAST;

  subtype POSITIVE_8  is INTEGER_8  range 1 .. INTEGER_8'LAST;

  subtype POSITIVE_16 is INTEGER_16 range 1 .. INTEGER_16'LAST;

  subtype POSITIVE_32 is INTEGER_32 range 1 .. INTEGER_32'LAST;

  subtype POSITIVE_64 is INTEGER_64 range 1 .. INTEGER_64'LAST;

  type UNSIGNED_8  is new INTEGER   range 0 .. (2 ** 8)  - 1;
  for  UNSIGNED_8'SIZE use 8;

  type UNSIGNED_16 is new INTEGER   range 0 .. (2 ** 16) - 1;
  for  UNSIGNED_16'SIZE use 16;

  type UNSIGNED_32 is range 0 .. 4_294_967_295;
  for  UNSIGNED_32'SIZE use 32;

  -- type UNSIGNED_64 can not execed INTEGER_64'LAST
  subtype UNSIGNED_64 is INTEGER_64 range 0 .. INTEGER_64'LAST; 

  type FLOAT_32 is new SHORT_FLOAT;
  for  FLOAT_32'SIZE use 32;

  type FLOAT_64 is new LONG_FLOAT;
  for  FLOAT_64'SIZE use 64;

end STANDARD_TYPES;


