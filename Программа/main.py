from mygame import *

LEVEL = ["----------------------------------------",
         "-ssssssssssssssssssssssssssssssssssssss-",
         "-                                      -",
         "-                                      -",
         "-                                      -",
         "-          +                           -",
         "-                                      -",
         "-                                      -",
         "-                        +             -",
         "-                                      -",
         "-        --                            -",
         "-                                     a-",
         "-      +                              a-",
         "-                                     a-",
         "-                                      -",
         "-d             ----                    -",
         "-               ss           +         -",
         "-                                      -",
         "-                                      -",
         "-     +      *                         -",
         "-                          ---         -",
         "-      www                             -",
         "-      ---                     e       -",
         "----------------------------------------"]


def main():
    w = MyGame(1280, 768, "cyan", LEVEL)
    w.objects(w)
    w.update()
    w.Keys("Up", "Left", "Right")
    w.run()


if __name__ == '__main__':
    main()
