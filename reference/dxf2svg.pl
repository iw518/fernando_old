#!/perl/bin/perl -w

#This is a Test for a convertion script.
#It reads an DXF file and transforms it into an SVG file

# Copyright David Montminy
# Licenced under GPL version 2 or greater. Copy at will.
# Please send comments to tron@info.polymtl.ca and keep this notice.

require 5.001;
#require "cgi-lib.pl";

#Static Variables
#$TMP_DIR="/tmp";


#Dynamic Variables. Define in main to Eliminate Warnings
my(
%FORM,              #The Form data
%cgi_cfn,           #Uploaded file client-provided name
%cgi_ct,            #Uploaded file content-type. May be unreliable
%cgi_sfn,           #Uploaded file name on the server
$ret,               #Return value for the ReadParse call in cgi-lib
$buf,               #Buffer for data read from disk
$Read_File_Name,
$Write_File_Name,
@File_Lines,

@Point_List,
$Number,            #ID_Type for DXF
$Loop,
#Data for objects
$Entity,
$LastEntity,
$Section,
$Var_Name,
$X_Coordinate,
$Y_Coordinate,
$Text_String,
$Class_Name,        #Name of Layer or Class
$X2_Radius,            #OR X-Axis Radius in case of ellipse
$Y2_Radius,
$Rotation,          #Rotation angle
$Color,
$Thickness,
$Point,
$X_Min,
$X_Max,
$Y_Min,
$Y_Max,
$Y_Mid,
$Display,
$Font,

@Layer_Name,
@Layer_Color

);

##########################################################################
##########################################################################
# Main program (start point)#
##########################################################################
##########################################################################


#@@@TODO: Parse the data from command-line or CGI input

#Start off by reading and parsing the CGI data. Save the return value.
#Pass reference to retreive the data, the filenames, and the content type.
#$ret= &ReadParse(\%FORM,\%cgi_cfn,\%cgi_ct,\%cgi_sfn);

#A bit of error checking never hurt anyone.
#if (!define $ret){
#   &CgiDie("Error in reading and parsing the CGI input");
#}  elsif (!$ret) {
#   print "Missing informations. Please Refill the Form.\n";
#}


#@@@TODO: Remove fixed names
#open (ERRORFILE, ">testerr.txt");
open (READFILE, "input.dxf") or die("error in reading ReadFile");
#print ERRORFILE "Opened Read File \n";
open (WRITEFILE, ">output.svg")or die("error in Writing WriteFile");
#print ERRORFILE "Opened WriteFile \n";
open (WRITECSS, ">output.css")or die("error in Writing CSSFile");
#print ERRORFILE "Opened Css File \nOpened all Files \n"";


##########################################################################
##########################################################################
# DXF Reading functions     #
##########################################################################
##########################################################################

$Text_String="";
$Section="";
$Display="";
$LastEntity = "";
$Entity ="";
$X_Coordinate = 0;
$Y_Coordinate = 0;
$Class_Name ='';
$X2_Radius = 0;
$Y2_Radius = 0;
$Rotation = 0;
$Color =  'black';
$Thickness = 1;
$Font="";
$Number = 999;
$Loop=1;
$Number =0;

#Write svg optimizations and base attributes
print WRITECSS "svg
{
color-rendering   : optimizeSpeed ;
image-rendering   : optimizeSpeed ;
shape-rendering   : optimizeSpeed ;
text-rendering    : optimizeSpeed ;
}
polyline
{
fill              : none ;
stroke            : black ;
}
text
{
fill              : none ;
font-family       : Arial ;
font-size         : 12 ;
stroke            : crimson ;
}" ;



while (<READFILE>)
      {
      $File_Line =$_;
      $Loop += 1;
### Check if "  int_Number"
      if ($Loop == 2)
         {
         $File_Line =~ /\d+/ ;
         $Number = $& ;
         $Loop=0;
         }
### If 0,Write and re-initialise everything at Zero
      elsif ( $Number == 0)
            {
            $File_Line =~ /\w*/ ;
            if ($& ne "")
               {
               if ( $Section eq "TABLES" )
                  {
                   if ($Entity eq "LAYER" )
                      {
			########################
			#Layer Defintion Section
			########################
                      &Write_Class($Class_Name,"",$Display,"","none","","","","","","","","","",$Color,"","","","","","",\*WRITECSS);
                      $Color = "";
                      $Display= "";
                      $Class_Name= "";
                      $X2_Radius = 0;
                      $Y2_Radius = 0;
                      $Rotation = 0;
                      $Color =  'black';
                      $Thickness = 1;
                      foreach $index (0 .. $#Point_List) {
                      delete $Point_List[$index];} }
                      }
                   elsif ( $Section eq "ENTITIES" )
                         {
    			    ##########################
    			    #Object definition Section
			    ##########################
                         if    ($Entity eq "POLYLINE")
                               {
                               $LastEntity = $Entity;
                               }
                         elsif ($Entity eq "INSERT" )
                               {
                               $LastEntity = "Reset";
                               }
                         elsif ($Entity eq "LWPOLYLINE" or $Entity eq "LEADER" )
                               {
                               &Write_Polyline( $Class_Name,$Color, $Color, $Thickness,\@Point_List,\*WRITEFILE );
                               $LastEntity = "Reset";
                               }
                         elsif ( ($Entity eq "VERTEX") and ($& ne "VERTEX") and ($LastEntity eq "POLYLINE"))
                               {
                               &Write_Polyline( $Class_Name,$Color, $Color, $Thickness,\@Point_List,\*WRITEFILE );
                               $LastEntity = "Reset";
                               }
                         elsif ( $Entity eq "ELLIPSE")
                               {
                               &Write_Ellipse( $Class_Name,$Rotation, $X_Coordinate, $Y_Coordinate, $X2_Radius, $Y2_Radius, $Color, $Color, $Thickness,\*WRITEFILE) ;
                               $LastEntity = "Reset";
                               }
                         elsif ( $Entity eq "CIRCLE")
                               {
                               &Write_Circle( $Class_Name,$Rotation, $X_Coordinate, $Y_Coordinate, $X2_Radius, $Color, $Color, $Thickness,\*WRITEFILE) ;
                               $LastEntity = "Reset";
                               }
                         elsif ( $Entity eq "RECT")
                               {
                               &Write_Rect( $Class_Name,$Rotation, $X_Coordinate, $Y_Coordinate, $X2_Radius, $Y2_Radius, $Color, $Color, $Thickness,\*WRITEFILE) ;
                               $LastEntity = "Reset";
                               }
                         elsif ( $Entity eq "LINE")
                               {
                               &Write_Line( $Class_Name,$X_Coordinate, $Y_Coordinate, $X2_Radius, $Y2_Radius, $Color, $Color, $Thickness,\*WRITEFILE) ;
                               $LastEntity = "Reset";
                               }
                         elsif ( $Entity eq "TEXT")
                               {
                               &Write_Text($Class_Name,$Text_String, $X_Coordinate, $Y_Coordinate, $Rotation,  $Font,  $Thickness, $Color, \*WRITEFILE) ;
                               $LastEntity = "Reset";
                               }
                   if ($LastEntity eq "Reset")
                      {
                      $Class_Name= "";
                      $X_Coordinate = 0;
                      $Y_Coordinate = 0;
                      $Text_String = '';
                      $X2_Radius = 0;
                      $Y2_Radius = 0;
                      $Rotation = 0;
                      $Color =  'black';
                      $Thickness = 1;
                      foreach $index (0 .. $#Point_List) {
                      delete $Point_List[$index];}
                      }
                   }
               }
               $Entity = $& ;
               }


    elsif ( $Entity eq "SECTION" )
       {
       ### If 2, it's Section Name
       if ( $Number == 2)
          {
           $File_Line =~ /[-\w]*/ ;
           if ( $Section eq "HEADER" )
                  {
                  &Write_Header($X_Min,$Y_Min,$X_Max,$Y_Max,\*WRITEFILE);
                  }
           $Section = $& ;
          }
       ### If 9, it's the variable Name
       elsif (($Number == 9) and ($Section eq "HEADER"))
             {
              $File_Line =~ /\w+/ ;
              $Var_Name = $& ;
             }
       elsif (($Number == 10) and ($Var_Name eq "EXTMIN"))
             {
              $File_Line =~ /\w*.*\w*/ ;
              $X_Min = $& ;
             }
       elsif (($Number == 20) and ($Var_Name eq "EXTMIN"))
             {
              $File_Line =~ /\w*.*\w*/ ;
              $Y_Min = $& ;
             }
      elsif (($Number == 10) and ($Var_Name eq "EXTMAX"))
             {
              $File_Line =~ /\w*.*\w*/ ;
              $X_Max = $& ;
             }
      elsif (($Number == 20) and ($Var_Name eq "EXTMAX"))
             {
              $File_Line =~ /\w*.*\w*/ ;
              $Y_Max = $& ;
              $Y_Mid = ($Y_Max + $Y_Min)/2 ;
             }
       }

    elsif ( $Entity eq "LAYER" )
       {
       ### If 2, it's the Layer Name
       if ( $Number == 2)
          {
           $File_Line =~ /\w*/ ;
           if ($& ne "" ) {$Class_Name = "*[class=\"$&\"]" ;}
          }
       ### If 6, it's the Line Type
       elsif ($Number == 6)
             {
              $File_Line =~ /\w+/ ;
              $Point = $& ;
             }
       ### If 62, it's the layer default Color
       elsif ($Number == "62")
             {
              $File_Line =~ /\w+/ ;
              if ($& eq "7") { $Color = "black"} ;
              if ($& < 0){ $Display = "none" };
             }
       ### If 290, it's the display or not property.
       elsif ($Number == "290")
             {
              $File_Line =~ /\w+/ ;
              if ($& eq "0") { $Display = "none"} ;
             }
       }


   elsif ( ($Section eq "ENTITIES")) #or ($Section eq "BLOCKS") or ($Section eq "OBJECTS")#)
       {
       ### If 1, it's Text format
       if ( $Number == 1 and $Entity eq "TEXT" )
         {

          $Text_String = $File_Line ;

# Code supposed to change the "%%201" into "�". Unicode Used for the DXF as well as the SVG
               $Text_String =~ s/%%(\d{3})/\&\#$1;/g;
#               $Text_String =~ s/%%201/\&\#144;/g;
#               $Text_String =~ s/%%206/\&\#215;/g;
#         print ERRORFILE "Text: $Text_String ";

          }

          ### If 6, it's LineType
        elsif ( $Number == 6)
        {
         $File_Line =~ /\w*/ ;
         #$Line_Type = $& ;          #@@@TODO: Any use??
         }

        ### If 8, it's Layer name (class name)
        elsif ( $Number == 8)
        {
         $File_Line =~ /[\w\-]*/ ;
         $Class_Name = $& ;
#        print ERRORFILE "Class: $& ";
         }

         ### If 10-39, it's x,y and z coordinates
         #@@@TODO: Maybe translate for z coordinates into scale. For now they are ignored.

         elsif ( $Number >= 10 and $Number <=29 and ($Entity ne "POLYLINE"))
         {
         ### If 10,20, or 30, it's x, y or z start coordinates
         # Except if Polyline, In which case the coordinates are just the next ones.
         if (  $Number == 10 )
            {
             $File_Line =~ /\w+.*\w*/ ;
             $X_Coordinate = $& ;
             }
         elsif ($Number == 20)
               {
                $File_Line =~ /\w+.*\w*/ ;
                $Y_Coordinate = $& ;
                $Y_Coordinate -= 2*($Y_Coordinate - $Y_Mid);
                $Point = join(',' , $X_Coordinate , $Y_Coordinate);
                push @Point_List, $Point;
               }
          elsif ($Number == 11 )
                {
                 $File_Line =~ /\w+.*\w*/ ;
                 $X2_Radius = $& ;
                }
          elsif ($Number == 21 )
                {
                 $File_Line =~ /\w+.*\w*/ ;
                 $Y2_Radius = $& ;
                }
          }
       ### If 40, additionnal information
       elsif ( $Number == 40)
             {
             $File_Line =~ /\w*/;
             # If Ellipse, Major to minor
             if ($Entity eq 'ELLIPSE')
                {
                $Y2_Radius = $File_Line ;
                }
                #@@@TODO: Do more with attribut 40 (other objets)
             }

       ### If 48,it's Line type Scale
       elsif ( $Number == 48)
             {
             #@@@TODO: Any use?
             # $File_Line =~ /\w*/
             # $Class_Name = $& ;
             }
       ### Text rotation angle
      elsif ( $Number == 50 and $Entity eq "TEXT")
             {
             #@@@TODO: Collect more useful information
              $File_Line =~ /[\w\-]*.*\w*/ ;
              $Rotation = $& ;
             }
       ### If 62, Color Type ,might be define BYLAYER (absent or 255) or BYBLOCK (zero) a Negative value indicate that the layer is turned off(but the color is ok).
       elsif ( $Number == 62)
             {
             #@@@TODO:  any use?
             $File_Line =~ /\w*/

             # If 255, just forget it.

             # Else, translate into HEX color.

             }
       ### @@@TODO: If  other??????
       }
#If EOF, exit loop.
}

&Write_Footer(\*WRITEFILE);

close (READFILE);
close (WRITEFILE);
close (WRITECSS);
##########################################################################
##########################################################################
# SVG Writing fonctions     #
##########################################################################
##########################################################################

##########################################################################
# Header writing fonction
##########################################################################

sub Write_Header{
    my( $X_Min,              #X_min
        $Y_Min,              #Y_min
        $X_Max,              #X_max
        $Y_Max               #Y_max
        ) = @_ ;
        my $File_name=pop;             #File Name to write to (or file descriptor)


#Data Fixed for Testing
#@@@TODO: Check for base viewport data and replace transform coord...
print $File_name "<?xml version=\"1.0\" standalone=\"no\"?> \n <?xml-stylesheet href=\"output.css\" type=\"text/css\"?> \n
<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.0//EN\" \"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd\"> \n
<svg width=\"100%\" height=\"100%\"  enableZoomAndPanControls=\"true\"> \n
#<g transform=\"translate(0,0) rotate(0) translate(0,0)\"> \n
"

}

##########################################################################
#Footer writing Fonction
##########################################################################
sub Write_Footer{
    my $File_name=pop;             #File Name to write to (or file descriptor)

print $File_name "</g> \n </svg>";
}

##########################################################################
# Ellipse writing fonction
##########################################################################
sub Write_Ellipse{
    my( $Class_Name,
        $Rotate,             #Rotation Angle
        $Cx,                 #X coordinate of the Center
        $Cy,                 #Y coordinate of the Center
        $Rx,                 #X-axis radius length
        $Ry,                 #Y-axis radius length
        $Fill,               #fill color
        $Stroke,             #stroke (line contour) color
        $Stroke_Width       #stroke width
        ) = @_ ;
        my $File_name=pop;


print $File_name " <ellipse";
if ($Class_Name ne "" ) {print $File_name " class=\"$Class_Name\" ";}
print $File_name " transform=\"translate($Cx $Cy)  rotate($Rotate)\" rx=\"$Rx\" ry=\"$Ry\" fill=\"$Fill\" stroke=\"$Stroke\" stroke-width=\"$Stroke_Width\" \/> \n";
}

##########################################################################
# Circle writing fonction
##########################################################################

sub Write_Circle{
    my( $Class_Name,
        $Cx,                 #X coordinate of the Center
        $Cy,                 #Y coordinate of the Center
        $R,                  #Axis radius length
        $Fill,               #fill color
        $Stroke,             #stroke (line contour) color
        $Stroke_Width,       #stroke width
        ) = @_ ;
        my $File_name=pop;


print $File_name " <circle";
if ($Class_Name ne "" ) {print $File_name " class=\"$Class_Name\" ";}
print $File_name " cx=\"$Cx\" cy=\"$Cy\" fill=\"$Fill\" stroke=\"$Stroke\" stroke-width=\"$Stroke_Width\" \/\> \n";

}

##########################################################################
# Rectangle writing fonction
##########################################################################

sub Write_Rect{
    my( $Class_Name,
        $X,                  #X coordinate of right up corner
        $Y,                  #Y coordinate of right up corner
        $Width,              #Width of the rectangle
        $Height,             #Height of the rectangle
        $Rx,                 #Axis of the rounded edges
        $Ry,                 #Axis of the rounded edges
        $Fill,               #fill color
        $Stroke,             #stroke (line contour) color
        $Stroke_Width,       #stroke width
         ) = @_ ;
        my $File_name=pop;


print $File_name " <rect";
if ($Class_Name ne "" ) {print $File_name " class=\"$Class_Name\" ";}
print $File_name " x=\"$X\" y=\"$Y\" width=\"$Width\" height=\"$Height\" fill=\"$Fill\" stroke=\"$Stroke\" stroke-width=\"$Stroke_Width\" \/\> \n";

}


##########################################################################
# Line writing fonction
##########################################################################

sub Write_Line{
    my( $Class_Name,
        $X1,                 #X start coordinate
        $Y1,                 #Y start coordinate
        $X2,                 #X end coordinate
        $Y2,                 #Y end coordinate
        $Fill,               #fill color
        $Stroke,             #stroke (line contour) color
        $Stroke_Width,       #stroke width
        ) = @_ ;
        my $File_name=pop;


print $File_name " <line ";
if ($Class_Name ne "" ) {print $File_name " class=\"$Class_Name\" ";}
print $File_name " x1=\"$X1\" y1=\"$Y1\" x2=\"$X2\" y2=\"$Y2\" fill=\"$Fill\" stroke=\"$Stroke\" stroke-width=\"$Stroke_Width\" \/\> \n" ;

}

##########################################################################
# Polyline writing fonction
##########################################################################

sub Write_Polyline{
    my( $Class_Name,
        $Fill,               #fill color
        $Stroke,              #stroke (line contour) color
        $Stroke_Width,        #stroke width

        $Point_List         #The list of points. Passed by reference
        ) = @_ ;
    my $File_name=pop;


print $File_name " <polyline";
if ($Class_Name ne "" ) {print $File_name " class=\"$Class_Name\" ";}
print $File_name "  points=\" ";
#@@@TODO: Use line attributes in SVG
# fill=\"$Fill\" stroke=\"$Stroke\" stroke-width=\"$Stroke_Width\"

#@@@TODO: Make sub_fonction work with polyline (or remove entirely) 
#&Write_Point_List($Point_List);

   my ( $Loop);            #loop variable (internal use)
    foreach $Point (@$Point_List)
            {
             print $File_name "$Point ";
             $Loop =+1;
             if ($Loop >= 5)
                {
                 $Loop = 0;
                  print $File_name "\n";
                }
            }


print $File_name " \" \/\> \n";
}

##########################################################################
# Polygon writing fonction
##########################################################################

sub Write_Polygon{
    my( $Fill,               #fill color
        $Stroke,              #stroke (line contour) color
        $Stroke_Width,        #stroke width

        $Point_List          #The list of points. Passed by reference
         ) = @_ ;
        my $File_name=pop;

print $File_name " <polygon ";
if ($Class_Name ne "" ) {print $File_name " class=\"$Class_Name\" ";}
print $File_name " fill=\"$Fill\" stroke=\"$Stroke\" stroke-width=\"$Stroke_Width\" points=\" ";
&Write_Point_List($Point_List);
print $File_name " \" \/\> \n";
}

##########################################################################
# Point Writing subfonction
# (For polyline and polygon)
##########################################################################
sub Write_Point_List{
  my(
        $Point_List          #The list of points. Passed by reference
        ) = @_ ;
        my $File_name=pop;

    my ( $Loop);            #loop variable (internal use)
    foreach $Point (@$Point_List)
            {
             print $File_name "$Point ";
             $Loop =+1;
             if ($Loop >= 10)
                {
                 $Loop = 0;
                  print $File_name "\n";
                }
            }
}

##########################################################################
# Text Fonction
##########################################################################

sub Write_Text{
    my( $Class_Name,         #Class Name
        $Text,               #The text string
        $X,                  #X coordinate of right up corner
        $Y,                  #Y coordinate of right up corner
        $Rotate,             #The rotation angle
        $Font,               #The font family
        $Font_Size,          #The font size
        $Fill                #fill color
        ) = @_ ;
        my $File_name=pop;

if($Text){
$Rotate = (-($Rotate)); #Reverse the angles
#Code to insert link to each (numeric) text zone.
if ($Class_Name eq "-15")
   {
   print $File_name "<a xlink:href=\"/cgi-bin/formulaire.cgi\?$Text\" target=\"resultat\" > \n";
   }
#@@@TODO: remove fixed font (Possible css external file candidate)
print $File_name " <text";
if ($Class_Name ne "" ) {print $File_name " class=\"$Class_Name\" ";}
print $File_name " transform=\"translate($X $Y) rotate($Rotate) \"  > \n";
print $File_name "$Text";
print $File_name "</text>";
#Close the link
if ($Class_Name eq "-15") {print $File_name "</a>";}
print $File_name "\n";
}
}
##########################################################################
##########################################################################
# CSS2 Writing fonctions     #
##########################################################################
##########################################################################

##########################################################################
# Class Fonction
##########################################################################

sub Write_Class{
    my( $Class_Name,         #Class Name
        $Color_Rendering,    #'SVG' attribute.                                        Value: auto | optimizeSpeed | optimizeQuality | inherit
        $Display,            # Display propertie.                                     Value: inline | block | list-item | run-in | compact | marker | table | inline-table | table-row-group | table-header-group | table-footer-group | table-row | table-column-group | table-column | table-cell | table-caption | none | inherit
        $Enable_Background,  # Background propertie.                                  Value: accumulate | new [ <x> <y> <width> <height> ] | inherit
        $Fill,               #Color Filling property.                                 Value: <paint> (See Specifying paint)
        $Fill_Opacity,       #Color Opacity level                                     Value: <opacity-value> | inherit
        $Fill_Rule,          #What parts of the canvas are included inside the shape. Value: nonzero | evenodd | inherit
        $Font_Family,        #Type of font used, including 'Backup' font              Value: [[ <family-name> | <generic-family> ],]* [<family-name> | <generic-family>] | inherit
        $Font_Size,          #Size of Font used                                       Value: <absolute-size> | <relative-size> | <length> | <percentage> | inherit
        $Font_Style,         #Style of Text                                           Value: normal | italic | oblique | inherit
        $Font_Variant,       #Variant of font                                         Value: normal | small-caps | inherit
        $Font_Weight,        #Weight(bold) of font                                    Value: normal | bold | bolder | lighter | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | inherit
        $Image_Rendering,    #'SVG' attribute.                                        Value: auto | optimizeSpeed | optimizeQuality | inherit
        $Shape_Rendering,    #'SVG' attribute.                                        Value: auto | optimizeSpeed | crispEdges | geometricPrecision | inherit
        $Stroke,             #Stroke(line) Color                                      Value: <color> (See Specifying paint)
        $Stroke_Linecap,     #specifies the shape to be used at the end (of a line)   Value: butt | round | square | inherit
        $Stroke_Linejoin,    #specifies the shape to be used at the corners           Value: miter | round | bevel | inherit
        $Stroke_Opacity,     #specifies the opacity of the painting operation         Value: <opacity-value> | inherit
        $Stroke_Width,       #The width of the stroke                                 Value: <length> | inherit
        $Text_Decoration,    #This property describes decorations that are added      Value: none | [ underline || overline || line-through || blink ] | inherit
        $Text_Rendering,     #'SVG' attribute.                                        Value: auto | optimizeSpeed | optimizeLegibility | geometricPrecision | inherit
        ) = @_ ;
        my $File_name=pop;

if ($Class_Name ne "")
{
print $File_name "$Class_Name \n";
print $File_name "{\n";
if ($Color_Rendering ne "")   { print $File_name "color-rendering   : $Color_Rendering ;\n";  }#<svg> attribute
if ($Display)           { print $File_name "display           : $Display ;\n";          }
if ($Enable_Background ne "") { print $File_name "enable-background : $Enable_Background ;\n";}
if ($Fill ne "")              { print $File_name "fill              : $Fill ;\n";             }
if ($Fill_Opacity ne "")      { print $File_name "fill-opacity      : $Fill_Opacity ;\n";     }
if ($Fill_Rule ne "")         { print $File_name "fill-rule         : $Fill_Rule ;\n";        }
if ($Font_Family ne "")       { print $File_name "font-family       : $Font_Family ;\n";      }
if ($Font_Size ne "")         { print $File_name "font-size         : $Font_Size ;\n";        }
if ($Font_Style ne "")        { print $File_name "font-style        : $Font_Style ;\n";       }
if ($Font_Variant ne "")      { print $File_name "font-variant      : $Font_Variant ;\n";     }
if ($Font_Weight ne "")       { print $File_name "font-weight       : $Font_Weight ;\n";      }
if ($Image_Rendering ne "")   { print $File_name "image-rendering   : $Image_Rendering ;\n";  }#<svg> attribute
if ($Shape_Rendering ne "")   { print $File_name "shape-rendering   : $Shape_Rendering ;\n";  }#<svg> attribute
if ($Stroke ne "")            { print $File_name "stroke            : $Stroke ;\n";           }
if ($Stroke_Linecap ne "")    { print $File_name "stroke-linecap    : $Stroke_Linecap ;\n";   }
if ($Stroke_Linejoin ne "")   { print $File_name "stroke-linejoin   : $Stroke_Linejoin ;\n";  }
if ($Stroke_Opacity ne "")    { print $File_name "stroke-opacity    : $Stroke_Opacity ;\n";   }
if ($Stroke_Width ne "")      { print $File_name "stroke-width      : $Stroke_Width ;\n";     }
if ($Text_Decoration ne "")   { print $File_name "text-decoration   : $Text_Decoration ;\n";  }
if ($Text_Rendering ne "")    { print $File_name "text-rendering    : $Text_Rendering ;\n";   }#<svg> attribute
print $File_name "}\n";
}

#@@@TODO: Add following properties and any other jugged necessary
#        $Stroke_Dasharray,   # Value: none | <dasharray> | inherit
#if ($Stroke_Dasharray ne "")  { print $File_name "stroke-dasharray  : $Stroke_Dasharray ;\n";
#        $Stroke_Miterlimit,  # Value: <miterlimit> | inherit
#if ($Stroke_Miterlimit ne "") { print $File_name "stroke-miterlimit : $Stroke_Miterlimit ;\n";
#        $Visibility          # Value: visible | hidden | collapse | inherit
#if ($Visibility ne "")        { print $File_name "visibility        : $Visibility ;\n";

}

##########################################################################
##########################################################################
# Misc Fonctions
##########################################################################
##########################################################################

####################################################
#Re-initialise Variables to nothing (unused for now)
####################################################
#@@@TODO: Make function usefull (make more than a test function)
sub Init{
    my( $Number         #Number of variables
        ) = @_ ;
for ($i=0;$i<$Number;$i++)
    {
    my $Variable=pop;
       $Variable="";
    }
}