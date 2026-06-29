import java.util.ArrayList;
import java.util.InputMismatchException;
import java.util.Scanner;

// A simple class to represent a shopping list item
class ShoppingItem {
    String name;
    double price;
    int quantity;

    public ShoppingItem(String name, double price, int quantity) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }

    public double getSubTotal() {
        return price * quantity;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ArrayList<ShoppingItem> shoppingList = new ArrayList<>();
        int itemNumber = 1;
        boolean continueShopping = true;

        while (continueShopping) {
            System.out.println("\n------------------------------------------------");
            System.out.printf("%-15s %s \n", "", "SHOPPING LIST");
            System.out.println("------------------------------------------------");
            System.out.println();

            System.out.println("Item " + itemNumber);
            System.out.println();

            String productName = "";
            double productPrice = 0.0;
            int productQuantity = 0;

            // Input product name
            System.out.print("Enter product name: ");
            productName = scanner.nextLine();

            // Input product price with error handling
            while (true) {
                System.out.print("Enter product price: ");
                try {
                    productPrice = scanner.nextDouble();
                    break; // Exit loop if input is valid
                } catch (InputMismatchException e) {
                    System.out.println("Invalid input. Please enter a number for the price.");
                    scanner.next(); // Consume the invalid input
                } finally {
                    scanner.nextLine(); // Consume leftover newline character
                }
            }

            // Input product quantity with error handling
            while (true) {
                System.out.print("Enter product quantity: ");
                try {
                    productQuantity = scanner.nextInt();
                    break; // Exit loop if input is valid
                } catch (InputMismatchException e) {
                    System.out.println("Invalid input. Please enter an integer for the quantity.");
                    scanner.next(); // Consume the invalid input
                } finally {
                    scanner.nextLine(); // Consume leftover newline character
                }
            }

            // Add the new item to the list
            shoppingList.add(new ShoppingItem(productName, productPrice, productQuantity));
            itemNumber++;

            System.out.println("\n------------------------------------------------");
            System.out.println("Do you want to add another Item?");
            System.out.print("Press 1 to continue and 0 to exit: ");

            int choice = -1;
            while (true) {
                try {
                    choice = scanner.nextInt();
                    if (choice == 0 || choice == 1) {
                        break;
                    } else {
                        System.out.print("Invalid choice. Please enter 0 or 1: ");
                    }
                } catch (InputMismatchException e) {
                    System.out.print("Invalid input. Please enter a number (0 or 1): ");
                    scanner.next(); // Consume the invalid input
                } finally {
                    scanner.nextLine(); // Consume leftover newline character
                }
            }

            if (choice == 0) {
                continueShopping = false;
            }
        }

        // Display SHOPPING SUMMARY for all items
        System.out.println("\n---");
        System.out.println("SHOPPING SUMMARY");
        System.out.println("---");
        double grandTotal = 0.0;
        if (shoppingList.isEmpty()) {
            System.out.println("Your shopping list is empty.");
        } else {
            int currentItemNum = 1;
            for (ShoppingItem item : shoppingList) {
                System.out.printf("Product Name %d: %s\t \t \t Price: %.2f X %d\t \t Sub-total = %.2f Baht\n",
                                  currentItemNum++, item.name, item.price, item.quantity, item.getSubTotal());
                grandTotal += item.getSubTotal();
            }
            System.out.println("------------------------------------------------");
            System.out.printf("%-50sGrand Total = %.2f Baht\n", "", grandTotal);
            System.out.println("------------------------------------------------");
        }

        scanner.close(); // Close the scanner to prevent resource leaks
        System.out.println("Thank you for shopping!");
    }
}