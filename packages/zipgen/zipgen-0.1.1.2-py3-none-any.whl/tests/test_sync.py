from unittest import TestCase, main
from io import BytesIO
from zipfile import ZipFile
from zipgen import ZipBuilder, COMPRESSION_STORED, COMPRESSION_DEFLATED, COMPRESSION_BZIP2, COMPRESSION_LZMA


class TestSync(TestCase):
    def test_add_file(self) -> None:
        """Tests file creation."""
        builder = ZipBuilder()
        io = BytesIO()

        # Contents
        content1 = b"This is COMPRESSION_STORED compressed. " * 128
        content2 = b"This is COMPRESSION_DEFLATED compressed. " * 128
        content3 = b"This is COMPRESSION_BZIP2 compressed. " * 128
        content4 = b"This is COMPRESSION_LZMA compressed. " * 128

        # Add four files with different compressions
        for buf in builder.add_file("file1.txt", BytesIO(content1), compression=COMPRESSION_STORED):
            io.write(buf)

        for buf in builder.add_file("file2.txt", BytesIO(content2), compression=COMPRESSION_DEFLATED):
            io.write(buf)

        for buf in builder.add_file("file3.txt", BytesIO(content3), compression=COMPRESSION_BZIP2):
            io.write(buf)

        for buf in builder.add_file("file4.txt", BytesIO(content4), compression=COMPRESSION_LZMA):
            io.write(buf)

        # End
        io.write(builder.end())

        # Check existence
        with ZipFile(io, "r") as file:
            self.assertEqual(
                file.namelist(),
                ["file1.txt", "file2.txt", "file3.txt", "file4.txt"],
            )

            self.assertEqual(file.read("file1.txt"), content1)
            self.assertEqual(file.read("file2.txt"), content2)
            self.assertEqual(file.read("file3.txt"), content3)
            self.assertEqual(file.read("file4.txt"), content4)

    def test_add_folder(self) -> None:
        """Test folder creation."""
        builder = ZipBuilder()
        io = BytesIO()

        # Add three folders
        io.write(builder.add_folder("test1"))
        io.write(builder.add_folder("test1/test2"))
        io.write(builder.add_folder("test1/test2/test3"))

        # End
        io.write(builder.end())

        # Check existence
        with ZipFile(io, "r") as file:
            self.assertEqual(
                file.namelist(),
                ["test1/", "test1/test2/", "test1/test2/test3/"],
            )

    def test_walk(self) -> None:
        """Test walk generator."""
        builder = ZipBuilder()
        io = BytesIO()

        # Walk tests files
        for buf in builder.walk("./", "/"):
            io.write(buf)

        # End
        io.write(builder.end())

        # Check existence
        with ZipFile(io, "r") as file:
            self.assertEqual(
                file.namelist(),
                ["test_sync.py", "test_async.py"],
            )

            for name in file.namelist():
                self.assertNotEqual(len(file.read(name)), 0)


if __name__ == "__main__":
    main()
