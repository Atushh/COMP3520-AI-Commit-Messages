public class Calculator {
    public static int add(int a, int b) {
        return a + b;
    }

    public static int subtract(int a, int b) {
        return a - b;
    }

    public static int multiply(int a, int b) {
        return a * b;
    }

    public static int divide(int dividend, int divisor) {
        if (divisor == 0) {
            throw new IllegalArgumentException("Divisor cannot be zero");
        }
        return dividend / divisor;
    }
    public static int remainder(int dividend, int divisor) {
    return dividend % divisor;
}
public static int absoluteValue(int value) {
    if (value == Integer.MIN_VALUE) {
        throw new ArithmeticException("Absolute value exceeds int range");
    }

    return Math.abs(value);
}
public static int max(int first, int second) {
    return Math.max(first, second);
}
public static int min(int first, int second) {
    return Math.min(first, second);
}
public static int square(int value) {
    return multiply(value, value);
}
public static int cube(int value) {
    return multiply(square(value), value);
}
public static boolean isPositive(int value) {
    return value > 0;
}
public static boolean isEven(int value) {
    return value % 2 == 0;
}
public static double fahrenheitToCelsius(double fahrenheit) {
    return (fahrenheit - 32.0) * 5.0 / 9.0;
}
public static double celsiusToFahrenheit(double celsius) {
    if (!Double.isFinite(celsius) || celsius < -273.15) {
        throw new IllegalArgumentException(
            "Celsius must be finite and at least -273.15"
        );
    }

    return celsius * 9.0 / 5.0 + 32.0;
}

public static boolean isBlank(String value) {
    return value.trim().isEmpty();
}

public static int countCharacters(String value) {
    return value.length();
}

public static String reverse(String value) {
    return new StringBuilder(value).reverse().toString();
}

public static int countVowels(String value) {
    int count = 0;

    for (int i = 0; i < value.length(); i++) {
        char character = Character.toLowerCase(value.charAt(i));

        if ("aeiou".indexOf(character) >= 0) {
            count++;
        }
    }

    return count;
}

public static boolean isPalindrome(String value) {
    return value.equalsIgnoreCase(reverse(value));
}

public static String trimWhitespace(String value) {
    return value.trim();
}

}