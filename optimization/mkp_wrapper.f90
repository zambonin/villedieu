program main
    implicit none
    external MTM

    integer :: i, n, solution, back, check, bound
    integer, dimension(10) :: prices, weights, placement
    integer, dimension(1) :: trucks1
    integer, dimension(2) :: trucks2
    integer, dimension(3) :: trucks3
    integer, dimension(4) :: trucks4

    solution = 0
    back = -1
    check = 1
    bound = 0

    prices = (/ 92, 57, 49, 68, 60, 43, 67, 84, 87, 72 /)
    weights = (/ 23, 31, 29, 44, 53, 38, 63, 85, 89, 82 /)

    n = SIZE(prices)

    trucks1 = (/ 165 /)
    trucks2 = (/ 70, 127 /)
    trucks3 = (/ 50, 81, 120 /)
    trucks4 = (/ 31, 37, 48, 152 /)

    call MTM(n, size(trucks1), prices, weights, trucks1, solution, &
        placement, back, check, bound)
    call pprint(placement)

    call MTM(n, size(trucks2), prices, weights, trucks2, solution, &
        placement, back, check, bound)
    call pprint(placement)

    call MTM(n, size(trucks3), prices, weights, trucks3, solution, &
        placement, back, check, bound)
    call pprint(placement)

    call MTM(n, size(trucks4), prices, weights, trucks4, solution, &
        placement, back, check, bound)
    call pprint(placement)

contains
    subroutine pprint(place)
        integer, dimension(10) :: place
        print "(a20, 1i5)", "Optimal solution:", solution
        print "(a20, 10i3)", "Items in each truck:", (place(i), i = 1, n)
        place = (/ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 /)
    end subroutine pprint
end program main
